from django.contrib import admin
from harvest_app.models import Crop, Field, Storage, Driver, Trailer, Vehicle, Harvest, HarvestVehicle, HarvestArchive


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ["name", "area", "crop"]
    list_filter = ["crop"]
    search_fields = ["name"]


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ["name", "capacity"]


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        "last_name",
        "phone_number",
        "professional_experience"
    ]
    list_filter = ["professional_experience"]
    search_fields = ["last_name"]


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ["trailer_type", "capacity", "license_plate"]
    list_filter = ["trailer_type", "capacity"]
    search_fields = ["license_plate"]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "vehicle_type",
        "model",
        "load_capacity",
        "license_plate"
    ]
    list_filter = ["vehicle_type"]
    search_fields = ["license_plate"]


class HarvestVehicleInline(admin.TabularInline):
    model = HarvestVehicle
    extra = 1


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ["date", "status", "field"]
    list_filter = ["status"]
    search_fields = ["field__name", "date__year"]
    inlines = [HarvestVehicleInline]


@admin.register(HarvestArchive)
class HarvestArchiveAdmin(admin.ModelAdmin):
    list_display = [
        "date", "field_name", "created_at"
    ]
