from rest_framework import serializers
from .models import Order, OrderItem, Coupon, OrderStatus

class OrderStatusUpdateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    status = serializers.CharField()
    def validate(self, data):
        order_id = data.get('order_id')
        status_name = data.get('status')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")
        
        try:
            status_obj = OrderStatus.objects.get(name__iexact=status_name)
        except OrderStatus.DoesNotExist:
            raise serializers.ValidationError("Invalid status")

        data['order'] = order
        data['status_obj'] = status_obj
        return data

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_price', 'items']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
    