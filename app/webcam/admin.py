from django.contrib import admin
from webcam import models

admin.site.register(models.Category)
admin.site.register(models.Webcam)
admin.site.register(models.Comment)
