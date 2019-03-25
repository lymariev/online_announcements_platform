from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=32, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategory')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Announcement(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_is_negotiable = models.BooleanField(default=False)
    last_activity = models.DateField(auto_now=True)
    is_hidden = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    in_favorites = models.ManyToManyField(User, related_name='in_favorites', blank=True)

    def __str__(self):
        return self.name


class AnnouncementImage(models.Model):
    image = models.ImageField(upload_to='images', blank=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
