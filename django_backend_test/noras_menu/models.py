# -*- encoding: utf-8 -*-

#STDLIB imports
import uuid
#Core Django Imports
from django.db import models
#Third Party apps imports

#Imports local apps


class Menu(models.Model):
	""" Set of option for the lunch of the day."""
	menu_uuid = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
	day = models.DateField(unique=True)

	def __unicode__(self):
		return u'%s' % (self.day)

	class Meta:
		permissions = (
            ('list_menu', 'List Menu'),
        )
	

class MenuItems(models.Model):
	"""Options of meals in the menu"""
	name = models.CharField(max_length=128)
	menu = models.ForeignKey(Menu)

	def __unicode__(self):
		return u'%s' % (self.name)

	class Meta:
		unique_together = ("name", "menu")

class UserSelectedLunch(models.Model):
	""" Special user's observations for his selected lunch option."""
	user = models.CharField(max_length=128)
	menu = models.ForeignKey(Menu)
	selected_item = models.ForeignKey(MenuItems)
	xl = models.BooleanField(default=False)
	observation = models.TextField()

	class Meta:
		unique_together = ("user", "menu")
		permissions = (
            ('list_selected', 'List Selected'),
        )
	


class Subscribers(models.Model):
	""" List of Subscribers. """
	email = models.EmailField(primary_key=True)
	full_name = models.CharField(max_length=128)
