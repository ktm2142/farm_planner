from django.urls import path
from harvest_app.views import FieldListView, CropListView

urlpatterns = [
    path("fields/", FieldListView.as_view(), name="field-list"),
    path("crops/", CropListView.as_view(), name="crop-list"),
]

app_name = "harvest_app"