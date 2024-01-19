from rest_framework.routers import DefaultRouter
from products import views

router = DefaultRouter()
router.register(r'product-images', views.ProductImageViewset)
router.register(r'products', views.ProductViewset)

urlpatterns = router.urls