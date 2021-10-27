from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet , send_company_email

companies_router = DefaultRouter()
companies_router.register("companies", viewset=CompanyViewSet, basename="companies")

urlpatterns = [
    path("", include(companies_router.urls)),
    path("send-email", send_company_email),
]