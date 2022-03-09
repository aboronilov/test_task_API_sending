from django.db import models


class Mailing(models.Model):
    beginning = models.DateTimeField(verbose_name='Начало рассылки')
    ending = models.DateTimeField(verbose_name='Окончание рассылки')
    text = models.TextField(verbose_name='Текст сообщения')
    mobile_codes = models.CharField('Коды мобильных операторов', max_length=50, blank=True)
    tags = models.CharField('Тэги для поиска', max_length=50, blank=True)

    def __str__(self):
        return f'Рассылка {self.id} от {self.beginning}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    phone = models.PositiveIntegerField(verbose_name='Мобильный телефон')
    code = models.PositiveIntegerField(verbose_name='Код мобильного оператора')
    tag = models.CharField(verbose_name='Тэги для поиска', max_length=50, blank=True)
    time_zone = models.CharField(verbose_name='Часовой пояс', max_length=10)

    def __str__(self):
        return f'Клиент {self.id} с номером {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    ACTIVE = "active"
    FAILED = "failed"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (FAILED, "Failed, pay attention"),
    ]

    date = models.DateTimeField(verbose_name='Дата отправки', auto_now_add=True)
    status = models.CharField(verbose_name='Статус отправки', max_length=6, choices=STATUS_CHOICES)
    message = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'Сообщение {self.id} с текстом {self.message} для {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


