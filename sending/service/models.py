from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Mailing(models.Model):
    beginning = models.DateTimeField(verbose_name='Начало рассылки')
    ending = models.DateTimeField(verbose_name='Окончание рассылки')
    text = models.TextField(verbose_name='Текст сообщения')
    mobile_codes = models.CharField('Коды мобильных операторов', max_length=50, blank=True)
    tags = models.CharField('Тэги для поиска', max_length=50, blank=True)

    @property
    def to_send(self):
        now = timezone.now()
        if self.beginning <= now <= self.ending:
            return True
        else:
            return False

    @property
    def sent_messages(self):
        return len(self.messages.filter(status='sent'))

    @property
    def messages_to_send(self):
        return len(self.messages.filter(status='proceeded'))

    @property
    def unsent_messages(self):
        return len(self.messages.filter(status='failed'))

    def __str__(self):
        return f'Рассылка {self.id} от {self.beginning}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    phone_regex = RegexValidator(regex=r'^7\w{10}$',
                                 message="номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)")
    phone = models.PositiveIntegerField(verbose_name='Мобильный телефон', validators=[phone_regex])
    code = models.PositiveIntegerField(verbose_name='Код мобильного оператора')
    tag = models.CharField(verbose_name='Тэги для поиска', max_length=50, blank=True)
    time_zone = models.CharField(verbose_name='Часовой пояс', max_length=10)

    def __str__(self):
        return f'Клиент {self.id} с номером {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    SENT = "sent"
    PROCEEDED = "proceeded"
    FAILED = "failed"

    STATUS_CHOICES = [
        (SENT, "Sent"),
        (PROCEEDED, "Proceeded"),
        (FAILED, "Failed"),
    ]

    date = models.DateTimeField(verbose_name='Дата отправки', auto_now_add=True)
    status = models.CharField(verbose_name='Статус отправки', max_length=15, choices=STATUS_CHOICES)
    message = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Сообщение {self.id} с текстом {self.message} для {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


