from django.views.generic import ListView
from harvest_app.models import Field


class FieldListView(ListView):
    model = Field
