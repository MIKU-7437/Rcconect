from rest_framework import viewsets


from users import serializers, models

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema(tags=['users']) 
# @extend_schema_view(
#     list=extend_schema(description='View list description'),
#     retrieve=extend_schema(description='View retrieve description'),
#     create=extend_schema(description='Create user'),
#     update=extend_schema(description='Update user'),
#     partial_update=extend_schema(description='Partial update user'),
#     destroy=extend_schema(description='Delete user'),
# )
class UserViewSet(viewsets.ModelViewSet):
    """
    enable the creation, retrieval, updating, and deletion of user profiles.

    Endpoints:
    - GET /users/: Retrieves a list of all users. This endpoint is typically used by administrators to oversee the user base.
    - GET /users/{id}/: Fetches a detailed view of a specific user by their ID. Useful for obtaining complete profile information, including links, documents, and contact information.
    - POST /users/: Allows for the creation of new user profiles. Required fields include username and email, among others specified in the UserSerializer.
    - PUT /users/{id}/: Fully updates an existing user profile. All user information must be provided anew.
    - PATCH /users/{id}/: Partially updates an existing user's profile. Only the fields provided in the request will be updated.
    - DELETE /users/{id}/: Removes a user profile from the system. Use with caution as this operation cannot be undone.

    Special Notes:
    - Some operations, such as creating or deleting a user, may be restricted based on the requester's permissions.
    - User data is sensitive and protected. Ensure that access to these endpoints is secured and compliant with data protection regulations.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerialzer


@extend_schema(tags=['users']) 
class PhoneViewSet(viewsets.ModelViewSet):
    
    queryset = models.Phone.objects.all()
    serializer_class = serializers.PhoneSerializer


@extend_schema(tags=['users']) 
class LinkViewSet(viewsets.ModelViewSet):

    queryset = models.Link.objects.all()
    serializer_class = serializers.LinkSerializer


@extend_schema(tags=['users']) 
class DocumentViewSet(viewsets.ModelViewSet):

    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer


@extend_schema(tags=['users']) 
class UserDetailViewSet(viewsets.ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerialzer
    lookup_field = "id"
