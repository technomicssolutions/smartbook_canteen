from django.db import models
from datetime import datetime


class Canteen(models.Model):

    name = models.CharField('Name', max_length=200, null=True, blank=True, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Canteen'

    def get_json_data(self):
        canteen_data = {
            'id': self.id,
            'name': self.name,
            
        }
        return canteen_data
    def set_attributes(self, canteen_details):
        self.name = canteen_details['name']
        self.save()
        return self   



