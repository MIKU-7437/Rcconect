from rest_framework import viewsets


from users import serializers, models


class UserViewSet(viewsets.ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerialzer


class PhoneViewSet(viewsets.ModelViewSet):

    queryset = models.Phone.objects.all()
    serializer_class = serializers.PhoneSerializer


class LinkViewSet(viewsets.ModelViewSet):

    queryset = models.Link.objects.all()
    serializer_class = serializers.LinkSerializer


class DocumentViewSet(viewsets.ModelViewSet):

    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer


class UserDetailViewSet(viewsets.ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerialzer
    lookup_field = "id"
