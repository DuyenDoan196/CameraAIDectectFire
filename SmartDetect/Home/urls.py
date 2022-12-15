from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'Home'
urlpatterns = [
    path('', views.RenderHome.as_view(), name='detect camera'),
    path('camera/', views.camera, name="camera")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
