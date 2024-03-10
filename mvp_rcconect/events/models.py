from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


STATUS_CHOICES = [
    ('active', 'Активен'),
    ('archived', 'В архиве'),
    ('processing', 'Идёт'),
]

# CATEGORY_CHOICES необходимо расширить/убрать совсем
CATEGORY_CHOICES = [
    ('concert', 'Концерт'),
    ('conference', 'Конференция'),
    ('workshop', 'Мастер-класс'),
    ('exhibition', 'Выставка'),
    ('sport', 'Спортивное событие'),
    ('party', 'Вечеринка'),
    ('webinar', 'Вебинар'),
    ('meeting', 'Встреча'),
    ('internship', 'Стажировка'),
    ('fest', 'Фестиваль'),
    ('hackathon', 'Хакатон'),
    ('ideathon', 'Идеатон'),
    ('case competition', 'Кейс-чемпионат'),
    ('contest', 'Олимпиада'),
    ('other', 'Другое'),
]

FORM_OF_PAYMENT_CHOICES = [
    ('free', 'Бесплатно'),
    ('rcoins', 'За RCoins'),
    ('paid', 'Платно'),
]


class EventManyToManyModel(models.Model):
    """Абстрактный класс для связи many-to-many для связи с Event"""

    class Meta:
        abstract = True

    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, null=True)


class Event(models.Model):

    description = models.TextField()
    organizers = models.ManyToManyField(
        "users.User", related_name="events", through="OrganizedEvents"
    )

    is_showed = models.BooleanField(default=True)
    holding_date_time = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=250, default='Онлайн')
    # tags = models.ManyToManyField('Tag')
    status = models.CharField(choices=STATUS_CHOICES,
                              default='active',
                              max_length=32)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    form_payment = models.CharField(
        choices=FORM_OF_PAYMENT_CHOICES,
        default='free',
        max_length=32
    )
    visit_cost = models.DecimalField(  # если добавлять цену,
        max_digits=10,                 # значит и дабавлять сам билет например
        decimal_places=2,              # через QR или просто статус "оплачено"
        default=0,
        validators=[
            MinValueValidator(
                0, 'Стоимость билета не может отрицательной'
            ),
            MaxValueValidator(
                10**6, 'Стоимость билета не может превышать 10^6'
            )
        ]
    )
    address = models.CharField(max_length=250, default="Онлайн")
    tags = models.ManyToManyField(
        "tags.Tag", related_name="events", through="EventTags"
    )

    class Meta:
        verbose_name = ("event",)
        verbose_name_plural = ("events",)

    def __str__(self) -> str:
        return (
            f'{self.holding_date_time} '
            f'{self.address} {", ".join(self.organizer.all())}'
        )


class OrganizedEvents(models.Model):

    organizer = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             null=True,
                             )
    event = models.ForeignKey('events.Event',
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='organized_events')


class EventImage(models.Model):

    height = models.IntegerField()
    width = models.IntegerField()
    image_type = models.CharField(max_length=5)
    url = models.URLField()
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='images')

    class Meta:
        verbose_name = ('image',)
        verbose_name_plural = ('images',)

    def __str__(self) -> str:
        return f'{self.event} - {self.height} x {self.width}'


class Post(models.Model):
    """Публикации партнеров о мероприятиях на сайте"""
    text = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,  # on_delete=models.CASCADE?
        null=True,
        related_name='posts'
    )
    source = models.ForeignKey(
        'users.Link',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='posts'
    )
    post_id = models.CharField(max_length=50)
    url = models.URLField()
    published_date_time = models.DateTimeField()

    class Meta:
        verbose_name = ('post',)
        verbose_name_plural = ('posts',)

    def __str__(self) -> str:
        return f'{self.event} - {self.author} - {self.published_date_time}'

    # organizer = models.ForeignKey(
    #     "users.User",
    #     on_delete=models.CASCADE,
    #     null=True,
    #     related_name="organized_events",
    # )


class EventTags(EventManyToManyModel):

    tag = models.ForeignKey(
        "tags.Tag",
        on_delete=models.CASCADE,
        null=True,
        related_name="event_tags",
    )


class EventLocation(models.Model):
    """Модель для адреса проведения мероприятия"""
    event = models.OneToOneField(
        'Event',
        on_delete=models.CASCADE,
        primary_key=True
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    comment = models.TextField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = ('event location',)

    def __str__(self) -> str:
        return f'Местоположение для {self.event}'
