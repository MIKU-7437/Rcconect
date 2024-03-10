from rest_framework import serializers


from users.models import User
from tags.models import Tag
from .models import Event, EventImage, OrganizedEvents, EventTags, Post
from users.serializers import UserSerialzer
from rest_framework import serializers

from .models import Event
from tags.serializers import TagSerializer
from mvp_rcconect.interfaces.serializers import ManyToManyModelSerializer


class EventImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventImage
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class EventSerializer(ManyToManyModelSerializer):

    organizers = UserSerialzer(many=True)
    tags = TagSerializer(many=True)
    images = EventImageSerializer(many=True)

    through_tables = {
        "organizers": {
            "through_table_model": OrganizedEvents,
            'right_model': User,
            "error_message": "У мероприятия должны быть организаторы",

        },
        "tags": {
            "through_table_model": EventTags,
            'right_model': Tag,
            "error_message": "У мероприятия должны быть теги",

        }
    }

    class Meta:
        model = Event
        fields = (
            "id",
            "description",
            "organizers",
            "tags",
            "holding_date_time",
            "address",
            "images",
        )

    # def update(self, instance, validated_data):
    #     organizers_data = validated_data.pop("organizers")

    #     organizers = instance.organizers.all()
    #     instance.description = validated_data.get("description", instance.description)
    #     instance.holding_date_time = validated_data.get(
    #         "holding_date_time", instance.holding_date_time
    #     )
    #     instance.address = validated_data.get("address", instance.address)

    #     for organizer in organizers:
    #         if not organizers_data:
    #             return Response(
    #                 status=status.HTTP_400_BAD_REQUEST,
    #                 data={"message": "У мероприятия не может не быть организатора"},
    #             )
    #         else:
    #             for organzier_data in organizers_data:
    #                 if organzier_data["id"] != organizer.id:
    #                     organizer_from_db = User.objects.filter(id=organzier_data["id"])
    #                     if not organizer_from_db.exists():
    #                         return Response(status=status.HTTP_400_BAD_REQUEST)
    #                     organizer = User.objects.get(id=organzier_data["id"])
    #                     OrganziedEvents.objects.create(
    #                         event=instance, organizer=organizer
    #                     )
