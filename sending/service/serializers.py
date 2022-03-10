from rest_framework import serializers
from .models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для клиентов
    """
    class Meta:
        model = Client
        exclude = ('phone_regex', )


class MailingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рассылки
    """
    class Meta:
        model = Mailing
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
