from django.urls import path
from .views import *

urlpatterns = [
    path("coupons.validate/", CouponValidationView.as_view(), name="validate-coupon"),
    path("history/",OrderHistoryView.as_view(), name='order-history'),
    path("coupons/", CouponListView.as_view(), name='coupons'),
    path("orders/<int:id>/", OrderDetailView.as_view(), name='order-detail'),
    path("update-status/", UpdateOrderStatusView.as_view(), name='update-order-status'),
    path("payment-methods/", PaymentMethodListView.as_view(), name='payment-methods'),
    path("cancel-order/<int:order_id>/", CancelOrderView.as_view(), name='cancel-order'),
]
