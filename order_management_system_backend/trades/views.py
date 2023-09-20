from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from trades.permissions import IsAdminOrSuperadminOrReadOnly, IsSuperadminOrReadOnly
from .models import Trade
from .serializers import TradeSerializer, TradeWithTotalSerializer, TradeUpdateSerializer
from datetime import datetime

class TradePagination(pagination.PageNumberPagination):
    page_size = 10  # Number of trades per page
    page_size_query_param = 'page_size'

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    pagination_class = TradePagination

    def get_permissions(self):
        if self.action == 'update':
            return [IsAdminOrSuperadminOrReadOnly()]
        elif self.action == 'destroy':
            return [IsSuperadminOrReadOnly()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return TradeWithTotalSerializer
        return TradeSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Trade.objects.filter(user=user).order_by('id')

        if user.is_staff or user.is_superuser:
            queryset = Trade.objects.all().order_by('id')
            user_qry = self.request.query_params.get('user')
            if user_qry:
                queryset = queryset.filter(user__id=user.id).order_by('id')

        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')
        buy_sell = self.request.query_params.get('buy_sell')
        symbol = self.request.query_params.get('symbol')
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            queryset = queryset.filter(date_of_execution__gte=start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            queryset = queryset.filter(date_of_execution__lte=end_date)
            
        buy_sell_choices = ['Buy', 'Sell']
        symbol_choices = ['AAPL', 'GOOGL', 'MSFT', 'SPY', 'QQQ', 'GLD', 'BTC', 'ETH', 'XRP', 'EUR/USD', 'GBP/JPY', 'USD/JPY', 'XAU', 'CL', 'NG', 'SPX', 'ES', 'TLT', 'AGG', 'DJI', 'IXIC', 'S&P 500', 'VTSAX', 'FBGRX']

        # Apply filters for buy/sell and symbol
        if buy_sell and buy_sell in buy_sell_choices:
            queryset = queryset.filter(buy_sell=buy_sell)
        
        if symbol and symbol in symbol_choices:
            queryset = queryset.filter(symbol_of_shares=symbol)

        return queryset

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.id

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class TradeUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff or request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return Response(
            {'message': 'You do not have permission to update this trade.'},
            status=status.HTTP_403_FORBIDDEN
        )