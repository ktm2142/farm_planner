from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from harvest_app.forms import (
    FieldCreateForm, CropCreateForm, StorageCreateForm,
    DriverCreateForm, TrailerCreateForm, VehicleCreateForm,
    HarvestCreateForm, HarvestVehicleCreateForm
)
from harvest_app.models import (
    Field, Crop, Storage,
    Driver, Trailer, Vehicle,
    Harvest, HarvestArchive, HarvestVehicle
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
    success_url = "/fields"


class CropListView(LoginRequiredMixin, ListView):
    model = Crop


class CropCreateView(LoginRequiredMixin, CreateView):
    model = Crop
    form_class = CropCreateForm
    success_url = "/crops"


class StorageListView(LoginRequiredMixin, ListView):
    model = Storage


class StorageCreateView(LoginRequiredMixin, CreateView):
    model = Storage
    form_class = StorageCreateForm
    success_url = "/storages"


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = Driver
    form_class = DriverCreateForm
    success_url = "/drivers"


class TrailerListView(LoginRequiredMixin, ListView):
    model = Trailer


class TrailerCreateView(LoginRequiredMixin, CreateView):
    model = Trailer
    form_class = TrailerCreateForm
    success_url = "/trailers"


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleCreateForm
    success_url = "/vehicles"


class HarvestListView(LoginRequiredMixin, ListView):
    model = Harvest


class HarvestCreateView(LoginRequiredMixin, CreateView):
    model = Harvest
    form_class = HarvestCreateForm


class HarvestDetailView(LoginRequiredMixin, DetailView):
    model = Harvest


class HarvestVehicleCreateView(LoginRequiredMixin, CreateView):
    model = HarvestVehicle
    form_class = HarvestVehicleCreateForm
    template_name = "harvest_app/harvest_vehicle_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["harvest"] = get_object_or_404(
            Harvest, pk=self.kwargs["pk"]
        )
        return kwargs

    # this method is for adding one or more vehicles to harvest
    def form_valid(self, form):
        form.save()
        action = self.request.POST.get("action")
        if action == "save_and_add":
            return redirect(self.request.path)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("harvest_app:harvest-detail", args=[self.kwargs["pk"]])


class HarvestArchiveList(LoginRequiredMixin, ListView):
    model = HarvestArchive
    context_object_name = "harvest_archive_list"
    template_name = "harvest_app/harvest_archive_list.html"
