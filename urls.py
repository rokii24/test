from django.urls import path
from .views import UploadImage

urlpatterns = [
    path('process/', UploadImage.as_view()),
    
]