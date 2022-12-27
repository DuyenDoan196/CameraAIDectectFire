from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .constant.config import ConfigWeb

app_name = 'Home'
urlpatterns = [
    path('', views.RenderHome.as_view(), name='detect camera'),
    path('camera/', views.cameraA, name="camera_a"),
    path('camera/', views.cameraB, name="camera_b"),
    path('camera/', views.cameraC, name="camera_c")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
