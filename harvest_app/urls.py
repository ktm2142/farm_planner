from django.urls import path
from harvest_app.views import FieldListView

urlpatterns = [
    path("fields/", FieldListView.as_view(), name="field-list")
]

app_name = "harvest_app"