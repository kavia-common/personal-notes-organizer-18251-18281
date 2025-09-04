from django.urls import path
from .views import (
    health,
    SignupView,
    LoginView,
    LogoutView,
    NoteListCreateView,
    NoteRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('health/', health, name='Health'),

    # Authentication
    path('auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

    # Notes
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroyView.as_view(), name='note-detail'),
]
