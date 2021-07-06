from django.urls import path, include
from transaction import views
import transaction
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('transaction', views.TransactionViewSet,)
router.register('itemdetails', views.TransactionLineItemDetailsViewSet,)
router.register('inventory', views.InventoryItemViewSet,)
urlpatterns = [
    # path('transaction/', views.TransactionView.as_view(),name='transaction'),
    path('',include(router.urls)),
]