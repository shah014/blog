from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):  # step10---Add these permissions to the Post views:
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

# 1.The custom IsOwnerOrReadOnly permission checks whether the requesting user
# is the owner of the given object

# 2.Only owners can perform actions such as updating or deleting a post. Non-owners
# can still retrieve a post, since this is a read-only action.

# 3.There is also a built-in IsAuthenticatedOrReadOnly permission................
# With this permission, any authenticated user can perform any request,
# Whereas non-authenticated users can perform only read-only requests.
