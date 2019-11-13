from django.contrib import admin

# Register your models here.

from headlines import models

admin.site.register(models.Headlines)
admin.site.register(models.Categories)
admin.site.register(models.Carousel)
admin.site.register(models.Comments)
admin.site.register(models.HeadlinesCollections)