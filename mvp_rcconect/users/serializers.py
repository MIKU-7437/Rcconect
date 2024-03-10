from rest_framework import serializers

from mvp_rcconect.interfaces.serializers import ManyToManyModelSerializer
from users import models


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Phone
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Link
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Document
        fields = "__all__"


class UserSerialzer(ManyToManyModelSerializer):

    phones = PhoneSerializer(many=True)
    links = LinkSerializer(many=True)
    documents = DocumentSerializer(many=True)

    through_tables = {
        "phones": {
            "through_table_model": models.UserPhones,
            "error_message": "У пользователя должны быть телефоны",
            "right_model": models.Phone,
        },
        "links": {
            "through_table_model": models.UserLinks,
            "error_message": "У пользователя должны быть ссылки",
            "right_model": models.Link,
        },
        "documents": {
            "through_table_model": models.UserDocuments,
            "error_message": "У пользователя должны быть документы",
            "right_model": models.Document,
        },
    }

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "city",
            "phones",
            "links",
            "documents",
        )

    def to_internal_value(self, data):
        if "id" not in data:
            return super().to_internal_value(data)
        return {"id": data["id"]}


class UserDetailSerialzer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        exclude = ("password",)
