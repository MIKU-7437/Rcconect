from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
        )

    def to_internal_value(self, data):
        if 'id' not in data:
            return super().to_internal_value(data)
        return {
            'id': data['id']
        }