from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    CategoryViewSet,
    OrderViewSet,
    CartViewSet,
)

router = DefaultRouter()

router.register("books", BookViewSet, basename="book")
router.register("categories", CategoryViewSet, basename="category")
router.register("orders", OrderViewSet, basename="order")
router.register("cart", CartViewSet, basename="cart")
urlpatterns = router.urls
