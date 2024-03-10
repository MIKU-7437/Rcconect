from django.db import models

# Create your models here.
class Tag(models.Model):
    """Теги мероприятий. Вешаются на каждый ивент и выбираются пользователем"""

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("tag",)
        verbose_name_plural = ("tags",)

    def __str__(self) -> str:
        return f"{self.name}"