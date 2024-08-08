from django.urls import path
from main.views import TextToImageView

urlpatterns = [
    path("text-to-image/", TextToImageView.as_view(), name="text-to-image"),
]
