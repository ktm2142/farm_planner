from django.views.generic import ListView
from harvest_app.models import Field, Crop, Storage, Driver, Trailer, Vehicle, Harvest, HarvestArchive


class FieldListView(ListView):
    model = Field


class CropListView(ListView):
    model = Crop


class StorageListView(ListView):
    model = Storage


class DriverListView(ListView):
    model = Driver


class TrailerListView(ListView):
    model = Trailer


class VehicleListView(ListView):
    model = Vehicle


class HarvestListView(ListView):
    model = Harvest


class HarvestArchiveList(ListView):
    model = HarvestArchive
    context_object_name = "harvest_archive_list"
    template_name = "harvest_app/harvest_archive_list.html"
