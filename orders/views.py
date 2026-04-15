from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Coupon
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
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
    formatted_time = format_datetimw(datetime.now())