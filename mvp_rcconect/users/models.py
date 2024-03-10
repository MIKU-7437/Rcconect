from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
)

from .validators import UnicodeUsernameValidator, validate_username

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]

# LIVE POSITION
UNIVERSITIES = ()

IMPORTANT_IN_LIVE = (
    ("Семья и дети", "Семья и дети"),
    ("Карьера и деньги", "Карьера и деньги"),
    ("Развлечения и отдых", "Развлечения и отдых"),
    ("Слова и влияние", "Слова и влияние"),
    ("Наука и исследования", "Наука и исследования"),
    ("Совершенствование мира", "Совершенствование мира"),
    ("Саморазвитие", "Саморазвитие"),
    ("Красота и искусство", "Красота и искусство"),
)
IMPORTANT_IN_PEOPLE = (
    ("Ум и креативность", "Ум и креативность"),
    ("Доброта и честность", "Доброта и честность"),
    ("Красота и здоровье", "Красота и здоровье"),
    ("Власть и богатство", "Власть и богатство"),
    ("Смелость и упорство", "Смелость и упорство"),
    ("Юмор и жизнелюбие", "Юмор и жизнелюбие"),
)

ATTITUDE_TO_SMOKING = (
    ("Резко негативное", "Резко негативное"),
    ("Негативное", "Негативное"),
    ("Компромиссное", "Компромиссное"),
    ("Нейтральное", "Нейтральное"),
    ("Положительное", "Положительное"),
)
ATTITUDE_TO_ALCOHOL = (
    ("Резко негативное", "Резко негативное"),
    ("Негативное", "Негативное"),
    ("Компромиссное", "Компромиссное"),
    ("Нейтральное", "Нейтральное"),
    ("Положительное", "Положительное"),
)


class User(AbstractUser):
    username_validators = [UnicodeUsernameValidator, validate_username]

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Обязательное поле. 150 символов или меньше. Только буквы, "
            "цифры и @/./+/-/_."
        ),
        validators=username_validators,
        error_messages={
            "unique": _("Пользователь с таким именем уже существует."),
        },
    )

    photo = models.ImageField(blank=True, null=True, upload_to="user_photos/")
    first_name = models.CharField(_("Имя"), max_length=150, blank=True)
    last_name = models.CharField(_("Фамилия"), max_length=150, blank=True)
    patronymic = models.CharField(_("Отчество"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"),
        max_length=254,
        unique=True,
        help_text=_("Обязательное поле. 254 символов или меньше."),
        error_messages={
            "unique": _("Пользователь с таким email уже существует."),
        },
    )
    status = models.CharField(max_length=40, null=True, blank=True)

    university = models.CharField(null=True, blank=True, max_length=150)
    faculty = models.CharField(null=True, blank=True, max_length=150)
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(date.today() - timedelta(days=365 * 120)),
            MaxValueValidator(date.today()),
        ],
    )
    # hobbies = models.TextField(null=True, blank=True, max_length=250)
    # favorite_tags = models.ManyToManyField('events.Tag', related_name='users')
    # live_positions
    important_in_live = models.CharField(
        max_length=32, null=True, blank=True, choices=IMPORTANT_IN_LIVE
    )
    important_in_people = models.CharField(
        max_length=32, null=True, blank=True, choices=IMPORTANT_IN_PEOPLE
    )
    attitude_to_smoking = models.CharField(
        max_length=32, null=True, blank=True, choices=ATTITUDE_TO_SMOKING
    )
    attitude_to_alcohol = models.CharField(
        max_length=32, null=True, blank=True, choices=ATTITUDE_TO_ALCOHOL
    )

    role = models.CharField(default=USER, choices=ROLES, max_length=9)

    group = models.CharField(
        _("Группа университета/класс школы"), max_length=100, blank=True, null=True
    )
    city = models.CharField(_("Город"), max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=350, blank=True, null=True)
    is_premium = models.BooleanField(_("Премиум-аккаунт"), default=False)
    is_company_account = models.BooleanField(_("Аккаунт компании"), default=False)
    links = models.ManyToManyField("Link", related_name="users", through="UserLinks")
    phones = models.ManyToManyField("Phone", related_name="users", through="UserPhones")
    documents = models.ManyToManyField(
        "Document", related_name="users", through="UserDocuments"
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.is_authenticated and self.role == MODERATOR

    @property
    def is_user(self):
        return self.is_authenticated and self.role == USER

    @property
    def age(self):
        if self.date_of_birth is None:
            return None
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    class Meta:
        verbose_name = ("user",)
        verbose_name_plural = ("users",)


class Phone(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Номер телефона должен быть в формате: '+999999999'. "
        "Допускается до 15 цифр.",
    )
    phone_number = models.CharField(
        _("Номер телефона"), validators=[phone_regex], max_length=16, unique=True
    )

    class Descriptions(models.TextChoices):
        HOME = "home", "Домашний"
        MOBILE = "mobile", "Мобильный"
        WORK = "work", "Рабочий"
        OTHER = "other", "Другой"

    description = models.CharField(
        _("Описание"), max_length=10, choices=Descriptions.choices
    )

    class Meta:
        verbose_name = ("phone",)
        verbose_name_plural = ("phones",)


class UserPhones(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)


class Company(models.Model):
    name = models.CharField(_("Название компании"), max_length=128)
    description = models.TextField(_("Описание компании"), max_length=512)
    activity_kinds = models.CharField(
        _("Род деятельности"), max_length=128
    )  # подумать над тегами
    is_owner = models.BooleanField(default=False)
    staff = models.ForeignKey(
        "User", on_delete=models.DO_NOTHING, related_name="company"
    )


class Link(models.Model):

    url = models.URLField(max_length=200)

    class Attachment(models.TextChoices):

        VK = "VK", "VK"
        TG = "TG", "Telegram"
        WEB = "WEB", "Web"

    attachment = models.CharField(max_length=3, choices=Attachment.choices)
    vk_domain = models.CharField(max_length=100, blank=True, null=True)
    to_parse = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("link",)
        verbose_name_plural = ("links",)


class UserLinks(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, null=True)


class Document(models.Model):

    number = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10)  # хз что это
    start_date = models.DateField()
    end_date = models.DateField()
    text_url = models.URLField()
    price = models.FloatField(null=True, blank=True)

    @property
    def is_valid(self):
        # TODO: перенести в метод validate() сериализатора
        return self.start_date <= date.today() <= self.end_date

    class Meta:
        verbose_name = ("document",)
        verbose_name_plural = ("documents",)


class UserDocuments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
