from rest_framework import serializers

from .models import Security, History


class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    secid = serializers.PrimaryKeyRelatedField(queryset=Security.objects.all())

    class Meta:
        model = History
        fields = '__all__'


class SummaryDataSerializer(serializers.Serializer):
    """Сериализатор для сводных данных о ценных бумагах и истории торгов"""
    secid = serializers.CharField(source='secid.secid')
    regnumber = serializers.CharField(source='secid.regnumber', allow_null=True)
    name = serializers.CharField(source='secid.name')
    emitent_title = serializers.CharField(source='secid.emitent_title', allow_null=True)
    tradedate = serializers.DateField()
    numtrades = serializers.FloatField()
    open = serializers.FloatField(allow_null=True)
    close = serializers.FloatField(allow_null=True)
