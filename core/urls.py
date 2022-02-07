from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'authors', views.AuthorViewset)
router.register(r'books', views.BookViewset)
router.register(r'stock', views.StockViewset)

urlpatterns = router.urls