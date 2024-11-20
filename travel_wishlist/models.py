from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    date_visited = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user_images/', null=True, blank=True)

    #create save method to override default save method
    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        
        super().save(*args, **kwargs)

    #delete method for deleting photo
    def delete_photo(self, photo):
        if default_storage.exists(photo):
            default_storage.delete(photo)

    #delete method for deleting photo when place is deleted
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)
        super().delete(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.name} visited: {self.visited} on {self.date_visited}. Notes: {notes_str}. with photo: {photo_str}'
        