from distutils.command.upload import upload
from email.mime import image
from io import BytesIO
from operator import mod
from traceback import print_exc # to resize
from PIL import Image # to work with images

from django.core.files import File # to save 
from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/' 

class Product(models.Model):

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return '' 
    
    def make_thumbnail(self, image, size=(400, 300)):
        img = Image.open(image)
        img.convert('RGB') # convert to rgb to check that it is not a transparent image
        img.thumbnail(size) # resize image

        thumb_io = BytesIO() # create a BytesIO object
        img.save(thumb_io, 'JPEG', quality=85) # save image to BytesIO object

        thumbnail = File(thumb_io, name=image.name) # create a resized file

        return thumbnail