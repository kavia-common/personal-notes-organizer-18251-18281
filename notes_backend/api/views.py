from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import SignupSerializer, LoginSerializer, NoteSerializer
from .permissions import IsOwner


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    """
    Health check endpoint.
    Returns a simple JSON indicating the server is running.
    """
    return Response({"message": "Server is up!"})


class SignupView(generics.CreateAPIView):
    """
    Create a new user account.

    Request body:
    - username: string (required)
    - email: string (optional)
    - password: string (required, validated by Django's password validators)

    Response:
    - 201 Created with user id, username, and email
    """
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
    Authenticate user with username and password and establish a session.

    Request body:
    - username: string
    - password: string

    Response:
    - 200 OK with basic user info on success
    - 400 Bad Request on invalid credentials
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response(
            {"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    Logout the current authenticated user by clearing the session.

    Response:
    - 204 No Content
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteListCreateView(generics.ListCreateAPIView):
    """
    List the authenticated user's notes or create a new note.

    GET:
      - Returns a paginated list of notes belonging to the requesting user.
    POST:
      - Creates a new note for the requesting user.

    Filters:
      - Optional query param 'archived' (true/false) to filter on is_archived.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Note.objects.filter(owner=self.request.user)
        archived = self.request.query_params.get("archived")
        if archived is not None:
            if archived.lower() in ("1", "true", "yes"):
                qs = qs.filter(is_archived=True)
            elif archived.lower() in ("0", "false", "no"):
                qs = qs.filter(is_archived=False)
        return qs


class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific note belonging to the authenticated user.

    Object-level permission IsOwner ensures users can only access their own notes.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Note.objects.all()

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
