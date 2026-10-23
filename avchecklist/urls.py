from django.conf import settings
from django.contrib import admin
from django.urls import path

from checklist.views import checklist

urlpatterns = [
    path("", checklist, name="checklist"),
    path(settings.ADMIN_URL, admin.site.urls),
]
