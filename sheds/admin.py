from django.contrib import admin

from .models import Day, Lesson

admin.site.register((Day, Lesson))
