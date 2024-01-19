from rest_framework.routers import DefaultRouter
from orders import views


router = DefaultRouter()

router.register('order-items/', views.OrderItemViewSet)
router.register('orders/', views.OrderViewSet)

urlpatterns = router.urls