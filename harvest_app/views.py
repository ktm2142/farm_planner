from django.views.generic import ListView
from harvest_app.models import Field, Crop, Storage


class FieldListView(ListView):
    model = Field


class CropListView(ListView):
    model = Crop


class StorageListView(ListView):
    model = Storage
