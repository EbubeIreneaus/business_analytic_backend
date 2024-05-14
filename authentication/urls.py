from django.urls import path
from . import views

urlpatterns = [
    path('', views.Auth.as_view()),
    path('resend_verification_email/', views.send_verify_email)
]