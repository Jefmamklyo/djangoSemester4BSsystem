# root level urls.py 
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("BSCreation.urls")),
    path("ledger/", include("ledger.urls")),
]