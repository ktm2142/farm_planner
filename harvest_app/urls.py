from django.urls import path
from harvest_app.views import (
    FieldListView, CropListView, StorageListView,
    DriverListView, TrailerListView, VehicleListView,
    HarvestListView, HarvestArchiveList, index,
    FieldCreateView, CropCreateView, StorageCreateView,
    DriverCreateView, TrailerCreateView, VehicleCreateView, HarvestCreateView, HarvestDetailView,
    HarvestVehicleCreateView, HarvestArchiveCreateView, HarvestArchiveDetailView, FieldUpdateView, FieldDeleteView,
    CropUpdateView, CropDeleteView, StorageUpdateView, StorageDeleteView, DriverDetailView, DriverUpdateView,
    DriverDeleteView, TrailerUpdateView, TrailerDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path("fields/", FieldListView.as_view(), name="field-list"),
    path("fields/create/", FieldCreateView.as_view(), name="field-create"),
    path("fields/<int:pk>/update/", FieldUpdateView.as_view(), name="field-update"),
    path("fields/<int:pk>/delete/", FieldDeleteView.as_view(), name="field-delete"),
    path("crops/", CropListView.as_view(), name="crop-list"),
    path("crops/create/", CropCreateView.as_view(), name="crop-create"),
    path("crops/<int:pk>/update/", CropUpdateView.as_view(), name="crop-update"),
    path("crops/<int:pk>/delete/", CropDeleteView.as_view(), name="crop-delete"),
    path("storages/", StorageListView.as_view(), name="storage-list"),
    path("storages/create/", StorageCreateView.as_view(), name="storage-create"),
    path("storages/<int:pk>/update/", StorageUpdateView.as_view(), name="storage-update"),
    path("storages/<int:pk>/delete/", StorageDeleteView.as_view(), name="storage-delete"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/details/", DriverDetailView.as_view(), name="driver-detail"),
    path("drivers/<int:pk>/update/", DriverUpdateView.as_view(), name="driver-update"),
    path("drivers/<int:pk>/delete/", DriverDeleteView.as_view(), name="driver-delete"),
    path("trailers/", TrailerListView.as_view(), name="trailer-list"),
    path("trailers/create/", TrailerCreateView.as_view(), name="trailer-create"),
    path("trailers/<int:pk>/update/", TrailerUpdateView.as_view(), name="trailer-update"),
    path("trailers/<int:pk>/delete/", TrailerDeleteView.as_view(), name="trailer-delete"),
    path("vehicles/", VehicleListView.as_view(), name="vehicle-list"),
    path("vehicles/create/", VehicleCreateView.as_view(), name="vehicle-create"),
    path("harvests/", HarvestListView.as_view(), name="harvest-list"),
    path("harvests/create/", HarvestCreateView.as_view(), name="harvest-create"),
    path("harvests/<int:pk>/", HarvestDetailView.as_view(), name="harvest-detail"),
    path(
        "harvests/<int:pk>/add-vehicle/",
        HarvestVehicleCreateView.as_view(),
        name="harvest-add-vehicle"),
    path(
        "harvests/archive/",
        HarvestArchiveList.as_view(),
        name="harvest-archive-list"
    ),
    path(
        "harvests/<int:pk>/add-to-archive/",
        HarvestArchiveCreateView.as_view(),
        name="add-to-archive"
    ),
    path(
        "harvests/archive/<int:pk>/",
        HarvestArchiveDetailView.as_view(),
        name="harvest-archive-detail"
    ),

]

app_name = "harvest_app"
