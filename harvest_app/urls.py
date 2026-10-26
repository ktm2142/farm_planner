from django.urls import path
from harvest_app.views import FieldListView, CropListView, StorageListView, DriverListView, TrailerListView, \
    VehicleListView

urlpatterns = [
    path("fields/", FieldListView.as_view(), name="field-list"),
    path("crops/", CropListView.as_view(), name="crop-list"),
    path("storages/", StorageListView.as_view(), name="storage-list"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("trailers/", TrailerListView.as_view(), name="trailer-list"),
    path("vehicles/", VehicleListView.as_view(), name="vehicle-list"),
]

app_name = "harvest_app"
