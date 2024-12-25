from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DataImportView, HistoryViewSet, SecurityViewSet, SummaryDataAPIView

router = DefaultRouter()
router.register(r'securities', SecurityViewSet)
router.register(r'histories', HistoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/summary-data/<str:tradedate>/', SummaryDataAPIView.as_view(), name='summary-data'),
    path('', DataImportView.as_view(), name='import_data'),
]
