from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=7, decimal_places=2)
    crop = models.ForeignKey(
        Crop,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["name"]

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
    hire_date = models.DateField(auto_now_add=True)
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
    driver = models.ForeignKey(
        Driver,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
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
    date = models.DateTimeField()
    field = models.ForeignKey(
        Field,
        on_delete=models.PROTECT
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.status} {self.date} {self.field}"
