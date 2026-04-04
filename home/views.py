from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import MenuCategory, MenuItem, Table
from .serializers import MenuCategorySerializer,MenuItemSerializer, TableSerializer
from .utils import get_today_operating_hours
from django.http import HttpResponse
from .serializers import MenuItemSerializer, IngredientSerializer
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

# Create your views here.
class TableDetailView(generics.RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

def show_today_hours(request):
    open_time, close_time = get_today_operating_hours()

    if open_time and close_time:
        return HttpResponse(f"Today open from {open_time} - {close_time}")
    else:
        return HttpResponse('Restaurant is closed today')

class FeaturedMenuItemListView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(is_featured=True)

class MenuItemIngredientView(RetrieveAPIView):
    serializer_class = IngredientSerializer
    def get_queryset(self):
        menu_item_id = self.kwargs['pk']
        return MenuItem.objects.get(id=menu_item_id).ingredients.all()

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},
                status=status.HTTP_400_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )