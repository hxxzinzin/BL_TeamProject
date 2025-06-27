from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import StoreViewSet

store_router = SimpleRouter()
store_router.register('stores', StoreViewSet)

urlpatterns = [
    path('', include(store_router.urls)),
]