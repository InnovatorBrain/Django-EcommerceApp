from django.contrib import admin
from django.db import models
from . import models

# Register your models here.

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']



admin.site.register(models.TaggedItem)
