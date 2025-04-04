from django.contrib import admin
# from .models import SampleModel
from .models import Book, Review

# Register your models here.
# admin.site.register(SampleModel)
admin.site.register(Book)
admin.site.register(Review)
