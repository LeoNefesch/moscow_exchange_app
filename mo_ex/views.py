from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views import View
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Security, History
from .serializers import HistorySerializer, SecuritySerializer, SummaryDataSerializer
from .utils import load_data


class SecurityViewSet(viewsets.ModelViewSet):
    """View для работы с информацией о ценных бумагах"""
    queryset = Security.objects.all().order_by("secid")
    serializer_class = SecuritySerializer


class HistoryViewSet(viewsets.ModelViewSet):
    """View для работы с историей торгов за произвольную дату"""
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class SummaryDataAPIView(APIView):
    """View для получения сводных данных о ценных бумагах и истории торгов за произвольную дату.
    Пример запроса:
    `http://127.0.0.1:8000/api/summary-data/?date=2024-12-23`"""

    @extend_schema(
        parameters=[
            OpenApiParameter(name='date',
                             description='Дата в формате ГГГГ-ММ-ДД',
                             required=False, type=str)
        ],
        responses=SummaryDataSerializer(many=True))
    def get(self, request, *args, **kwargs):
        query_date = request.query_params.get('date')
        tradedate = parse_date(query_date) if query_date else now().date()
        if not tradedate:
            raise ValidationError({
                'detail': 'Неверный формат даты. Ожидается ГГГГ-ММ-ДД.'})
        history_records = History.objects.filter(tradedate=tradedate).select_related('secid')

        if not history_records.exists():
            return Response({"detail": "В БД нет записей на указанную дату."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SummaryDataSerializer(history_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DataImportView(View):
    """View для загрузки данных из внешнего источника."""
    def get(self, request):
        return render(request, "mo_ex/import_data.html")

    def post(self, request):
        try:
            load_data()
            return JsonResponse({"status": "success", "message": "Данные успешно загружены!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
