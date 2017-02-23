# -*- encoding: utf-8 -*-

#STDLIB imports

#Core Django Imports
from django.db import models
#Third Party apps imports

#Imports local apps


class Menu(models.Model):
	""" Set of option for the lunch of the day."""
	day = models.DateField(primary_key=True)

class MenuItems(models.Model):
	"""Options of meals in the menu"""
	name = models.CharField(max_length=128)
	menu = models.ForeignKey(Menu)

	class Meta:
		unique_together = ("name", "menu")

class UserSelectedLunch(models.Model):
	""" Special user's observations for his selected lunch option."""
	user = models.CharField(max_length=128)
	selected_item = models.ForeignKey(MenuItems)
	xl = models.BooleanField()
	observation = models.TextField()

	class Meta:
		unique_together = ("user", "selected_item")

class Subscribers(models.Model):
	""" List of Subscribers. """
	email = models.EmailField(primary_key=True)
	full_name = models.CharField(max_length=128)
	