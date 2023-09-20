from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TradeViewSet, TradeUpdateAPIView

router = DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trade')

urlpatterns = [
    path('', include(router.urls)),
    path('trades/<int:pk>/update/', TradeUpdateAPIView.as_view(), name='trade-update')
]
