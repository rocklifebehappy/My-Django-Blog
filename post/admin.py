from django.contrib import admin
from .models import Categories, Post, Subscribers, Contact

# Register your models here.
admin.site.register(Post)
admin.site.register(Categories)
admin.site.register(Subscribers)
admin.site.register(Contact)
