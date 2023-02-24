from django.contrib import admin
from django.urls import include, path

from core.urls import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
