from django.urls import path
from harvest_app.views import FieldListView, CropListView, StorageListView, DriverListView, TrailerListView, \
    VehicleListView, HarvestListView, HarvestArchiveList, index, FieldCreateView, CropCreateView

urlpatterns = [
    path("", index, name="index"),
    path("fields/", FieldListView.as_view(), name="field-list"),
    path("fields/create/", FieldCreateView.as_view(), name="field-create"),
    path("crops/", CropListView.as_view(), name="crop-list"),
    path("crops/create/", CropCreateView.as_view(), name="crop-create"),
    path("storages/", StorageListView.as_view(), name="storage-list"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("trailers/", TrailerListView.as_view(), name="trailer-list"),
    path("vehicles/", VehicleListView.as_view(), name="vehicle-list"),
    path("harvests/", HarvestListView.as_view(), name="harvest-list"),
    path(
        "harvests/archive/",
        HarvestArchiveList.as_view(),
        name="harvest-archive-list"
    ),
]

app_name = "harvest_app"
