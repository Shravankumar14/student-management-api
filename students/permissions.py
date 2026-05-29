from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # POST, PUT, DELETE
        return request.user and request.user.is_staff


class CanDeleteOnlyECEStudent(
    BasePermission
):

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        if request.method == 'DELETE':

            return obj.branch == 'ECE'

        return True