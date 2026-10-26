from django.urls import path
from harvest_app.views import FieldListView, CropListView, StorageListView

urlpatterns = [
    path("fields/", FieldListView.as_view(), name="field-list"),
    path("crops/", CropListView.as_view(), name="crop-list"),
    path("storages/", StorageListView.as_view(), name="storage-list"),
]

app_name = "harvest_app"