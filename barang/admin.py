from django.contrib import admin
from .models import *

# Get all model classes from models.py
model_classes = [model for model in vars().values() if isinstance(model, type) and issubclass(model, models.Model)]

# Register all model classes to the admin site
for model_class in model_classes:
    if not model_class._meta.abstract:
        try:
            admin.site.register(model_class)
        except admin.sites.AlreadyRegistered:
            pass
