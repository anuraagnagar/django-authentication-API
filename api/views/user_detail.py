from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.authentication import TokenAuthenticationCookie
from api.models import Users
from api.serializers import UserDetailSerializer


class UserDetailView(RetrieveUpdateAPIView):
    """
    API endpoint for retrieving user profile details.
    * Requires token-based authentication.

    Allow Methods:
    # GET: Retrieve and return the user's profile details.
    # PUT: update and return the success HTTP response.
    """

    authentication_classes = [TokenAuthenticationCookie]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = Users.objects.all()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle GET requests to retrieve user profile details.

        Return Type -> HttpResponse():
        # A JSON response containing user profile details.
        """
        user = getattr(request, "user", None)
        serializer = self.get_serializer(user)

        response_data = {
            "status": status.HTTP_200_OK,
            "message": _("Profile successfully loaded."),
            "data": serializer.data,
        }
        return Response(response_data, status.HTTP_200_OK)

    def put(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle PUT requests to update user profile.

        Return Type -> HttpResponse():
        # A JSON response indicating the update status.
        """

        data = getattr(request, "data", None)
        profile = get_object_or_404(self.get_queryset(), id=request.user.id)

        # Pass instance to the serializer when updating.
        serializer = self.get_serializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "status": status.HTTP_200_OK,
            "message": _("Your profile successfully updated."),
        }
        return Response(response_data, status.HTTP_200_OK)
