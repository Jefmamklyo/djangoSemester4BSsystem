# root level urls.py 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("BSCreation.urls")),
    path("merkleTree/", include("merkleTree.urls")),
]