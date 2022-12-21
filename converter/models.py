from django.db import models
from django.urls import reverse

# Create your models here.
class TagsModel(models.Model):
    tag_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag_name
    
    class Meta:
        verbose_name_plural = "Tags"

class PostModel(models.Model):
    author = models.CharField(max_length=200)
    tags = models.ManyToManyField(TagsModel)
    transcript = models.TextField()
    slug = models.CharField(max_length=400, null=False, db_index=True, unique=True)
    date = models.DateField(auto_now=True)
    language = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    thumbnail = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500, unique=True)

    def get_absolute_url(self):
        return reverse("post_url", args={self.slug})

    def __str__(self):
        return self.title

