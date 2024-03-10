from django.db import models
from rest_framework import serializers, response, status


class ThroughTablesDBWorker:
    """Класс предназначен для работы с through tables (many-to-many связей)
    Модель, с которой связан модель model. К примеру, для Event - User.
    Подразумевается связь m2m как левая сущность (Event) - правая сущность (User)
    """

    def __init__(
        self, serializer: serializers.ModelSerializer, right_model: models.Model
    ):
        self.right_model = right_model
        self.serializer = serializer

    def add_m2m_entity_if_id_exist_in_db(
        self, instance_name: str, left_instance: models.Model, entities: dict
    ) -> None:
        """Добавляет модель entity в through table, если id сущности существует в базе данных

        Args:
            created_instance (models.Model): Модель, для которой создаем связь, напр. Events
            entities (dict): Сущности, для которых существует m2m связь
        """
        through_table_model = self.__get_through_table_model(instance_name)
        if not entities:
            return self.__bad_request(instance_name)
        for entity_data in entities:
            try:
                entity_id = entity_data.get("id")
                right_entity, _ = self.right_model.objects.get(id=entity_id)
            except self.right_model.DoesNotExist:
                right_entity = self.right_model.objects.create(**entity_data)

            _, left_field, right_field = through_table_model._meta.get_fields()
            data = {
                left_field.name: left_instance,
                right_field.name: right_entity,
            }
            through_table_model.objects.create(**data)

    def __get_through_table_model(self, entity: str) -> models.Model:
        """Возвращает модель through table и сообщение об ошибке для сущности m2m

        Args:
            entity (str): Название сущности из сериализатора (Meta.fields)

        Returns:
            models.Model: Модель through table
        """
        return self.serializer.through_tables[entity]["through_table_model"]

    def __bad_request(self, entity: str) -> response.Response:
        """Возвращает сообщение об ошибке для сущности m2m

        Args:
            entity (str): Название сущности из сериализатора (Meta.fields)

        Returns:
            str: Сообщение об ошибке
        """
        return response.Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"message": self.serializer.through_tables[entity]["error_message"]},
        )


class ManyToManyModelSerializer(serializers.ModelSerializer):
    """Абстрактный класс для CRUD методов для моделей с m2m связями"""

    through_tables: dict[str, dict] = {}
    """
    {
        "organizers": {
            "through_table_model": OrganziedEvents,
            "error_message": "У мероприятия должны быть организаторы",
            'right_model': User
            'must_be_created': True
        },
        "tags": {
            "through_table_model": EventTags,
            "error_message": "У мероприятия должны быть теги",
            'right_model': Tag,
            'must_be_created': True
        }
    }
    """

    class Meta:
        abstract = True
        model: models.Model = None

    def get_db_worker(self, right_model: models.Model) -> ThroughTablesDBWorker:
        db_worker = ThroughTablesDBWorker(serializer=self, right_model=right_model)
        return db_worker

    def _extract_m2m_entities_data(self, validated_data: dict) -> dict:
        """Извлекает m2m поля из json запроса и возвращает их в виде таблицы (итератор списков)"""
        data = dict()
        print(validated_data)
        for entity in self.through_tables:
            if entity in validated_data:
                data[entity] = validated_data.pop(entity)

        return data

    def create(self, validated_data):

        m2m_entities = self._extract_m2m_entities_data(validated_data)
        left_instance = self.Meta.model.objects.create(**validated_data)

        for entity in m2m_entities:
            db_worker = self.get_db_worker(self.through_tables[entity]["right_model"])
            db_worker.add_m2m_entity_if_id_exist_in_db(
                entity, left_instance, m2m_entities[entity]
            )
        return left_instance
