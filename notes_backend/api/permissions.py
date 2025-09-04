from rest_framework.permissions import BasePermission


# PUBLIC_INTERFACE
class IsOwner(BasePermission):
    """
    Only allows owners of an object to access/modify it.
    Read and write operations require ownership.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)
