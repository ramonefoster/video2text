from django.contrib import admin
from .models import PostModel, TagsModel

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title",)

class TagAdmin(admin.ModelAdmin):
    list_display = ("tag_name", )

#Dispositivos
admin.site.register(PostModel, PostAdmin)

#Reports
admin.site.register(TagsModel, TagAdmin)