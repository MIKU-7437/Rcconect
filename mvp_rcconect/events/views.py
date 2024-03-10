from rest_framework import status
from rest_framework.views import Response
from rest_framework import viewsets

from events import models

from events import serializers
# from tags.serializers import TagSerializer
from users.models import User


class EventViewSet(viewsets.ModelViewSet):

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

    def create(self, request, *args, **kwargs):
        organizers = request.data['organizers']

        if organizers:
            for organizer in organizers:
                if not User.objects.filter(id=organizer['id']).exists():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': f'Пользователь с id = {organizer["id"]} не найден'})
            return super().create(request, *args, **kwargs)


class EventImageViewSet(viewsets.ModelViewSet):

    queryset = models.EventImage.objects.all()
    serializer_class = serializers.EventImageSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

# class TagViewSet(viewsets.ModelViewSet):