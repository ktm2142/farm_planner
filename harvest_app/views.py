from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from harvest_app.forms import FieldCreateForm
from harvest_app.models import (
    Field, Crop, Storage,
    Driver, Trailer, Vehicle,
    Harvest, HarvestArchive
)


def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_visits": num_visits + 1
    }

    return render(request, "harvest_app/index.html", context=context)


class FieldListView(LoginRequiredMixin, ListView):
    model = Field


class FieldCreateView(LoginRequiredMixin, CreateView):
    model = Field
    form_class = FieldCreateForm
    success_url = "/"


class CropListView(LoginRequiredMixin, ListView):
    model = Crop


class StorageListView(LoginRequiredMixin, ListView):
    model = Storage


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver


class TrailerListView(LoginRequiredMixin, ListView):
    model = Trailer


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle


class HarvestListView(LoginRequiredMixin, ListView):
    model = Harvest


class HarvestArchiveList(LoginRequiredMixin, ListView):
    model = HarvestArchive
    context_object_name = "harvest_archive_list"
    template_name = "harvest_app/harvest_archive_list.html"
