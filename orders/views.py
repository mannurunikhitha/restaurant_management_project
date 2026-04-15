from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Coupon
from rest_framework.permissions import IsAuthenticated
from .models import Order, PaymentMethod, OrderStatus
from .serializers import OrderSerializer, OrderStatusUpdateSerializer, PaymentMethodSerializer
from .utils import generate_coupon_code, send_order_confirmation_email, generate_unique_order_id
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Coupon
from .serializers import CouponSerializer
from datetime import datetime
from restaurant_management.utils import format_datetimw

# Create your views here.
class CouponValidationView(APIView):
    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "Coupon code is requires"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoneNotExist:
            return Response(
                {"error": "Invalid coupon code"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        today = timezone.now().date()

        if not coupon.is_active:
            return Response(
                {"error": "Coupon is inactive"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if not (coupon.valid_from <= today <= coupon.valid_until):
            return Response(
                {"error": "Coupon expired or not yet valid"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                "message": "Coupon is valid",
                "discount_percentage": coupon.discount_percentage
            },
            status = status.HTTP_200_OK
        )

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

class GenerateCouponView(APIView):
    def get(self, request):
        code = generate_coupon_code()
        return Response({"coupon_code": code})

class CouponListView(ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

def create_order(request):
    order = Order.objects.create(
        order_id=generate_unique_order_id(Order)
    )

def some_view(request):
    formatted_time = format_datetime(datetime.now())

class UpdateOrderStatusView(APIView):
    def put(self, request):
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data['order']
            status_obj = serializer.validated_data['status_obj']
            order.status = status_obj
            order.save()
            return Response({
                "message": "Order status update successfully",
                "order_id": order.id,
                "new_status": status_obj.name
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentMethodListView(ListAPIView):
    serializer_class = PaymentMethodSerializer
    def get_queryset(self):
        return PaymentMethod.objects.filter(is_active=True)

class CancelOrderView(APIView):
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoneNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_BAD_REQUEST
            )
        if order.user != request.user:
            return Response(
                {"error": "You are not allowed to cancel this order"},
                status=status.HTTP_403_FORBIDDEN
            )
        if order.status and order.status.name.lower() == 'completed':
            return Response(
                {"error": "Completed orders cannot be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            cancelled_status = OrderStatus.objects.get(name__iexact='cancelled')
        except OrderStatus.DoneNotExist:
            return Response(
                {"error": "Cancelled status not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        order.status = cancelled_status
        order.save()
        return Response(
            {"message": "Order cancelled successfully"},
            status=status.HTTP_200_OK
        )