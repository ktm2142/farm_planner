from django.db import models, transaction


class Crop(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ["area"]

    def __str__(self):
        return f"{self.name} x {self.area} ha"


class Storage(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    class Meta:
        ordering = ["-capacity"]

    def __str__(self):
        return f"{self.name} x {self.capacity} tons"


class Driver(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=20)
    hire_date = models.DateField()
    professional_experience = models.IntegerField()

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.last_name} {self.phone_number}"


class Trailer(models.Model):
    TRAILER_TYPE_CHOICES = [
        ("grain_cart", "Grain cart"),
        ("tipper_trailer", "Tipper trailer"),
        ("grain_semi_trailer", "Grain semi-trailer"),
        ("self_loading_hay_trailer", "Self loading hay trailer"),
    ]
    trailer_type = models.CharField(
        max_length=50,
        choices=TRAILER_TYPE_CHOICES
    )
    capacity = models.IntegerField()
    license_plate = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ["trailer_type"]

    def __str__(self):
        return f"{self.trailer_type} {self.license_plate} {self.capacity}"


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ("combine_harvester", "Combine Harvester"),
        ("tractor", "Tractor"),
        ("truck", "Truck"),
    ]
    vehicle_type = models.CharField(
        max_length=50,
        choices=VEHICLE_TYPE_CHOICES
    )
    model = models.CharField(max_length=255)
    load_capacity = models.IntegerField(
        blank=True,
        null=True,
    )
    license_plate = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ["vehicle_type"]

    def __str__(self):
        return (f"{self.vehicle_type}"
                f" {self.model} "
                f"{self.license_plate}"
                )


class Harvest(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="scheduled"
    )
    start_date = models.DateTimeField()
    field = models.ForeignKey(
        Field,
        on_delete=models.PROTECT
    )
    crop = models.ForeignKey(
        Crop,
        on_delete=models.PROTECT
    )
    vehicles = models.ManyToManyField(
        Vehicle,
        through="HarvestVehicle",
        related_name="harvests"
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.status} {self.start_date} {self.field}"

    def save(self, *args, **kwargs):
        if self.pk and self.status == "completed":
            self.complete()
            return
        super().save(*args, **kwargs)

    def complete(self):
        vehicles = ", ".join(
            f"{assignment.vehicle.license_plate} "
            f"({assignment.driver.last_name})"
            for assignment in self.assignments.select_related(
                "vehicle",
                "driver"
            )
        )
        with transaction.atomic():
            HarvestArchive.objects.create(
                start_date=self.start_date,
                field_name=self.field.name,
                crop_name=self.crop,
                storage_name=self.storage.name,
                vehicles_info=vehicles,
            )
            self.delete()


class HarvestArchive(models.Model):
    start_date = models.DateTimeField()
    field_name = models.CharField(max_length=255)
    crop_name = models.CharField(max_length=255)
    storage_name = models.CharField(max_length=255)
    vehicles_info = models.TextField()
    end_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return (f"Harvest from {self.start_date} to "
                f"{self.end_date} on {self.field_name}")


class HarvestVehicle(models.Model):
    harvest = models.ForeignKey(
        Harvest,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT
    )
    trailer = models.ForeignKey(
        Trailer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.vehicle} - {self.driver}"
