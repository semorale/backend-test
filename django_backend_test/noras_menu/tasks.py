# -*- encoding: utf-8 -*-

#app_mail/tasks.py
import requests
import simplejson as json

from django_backend_test.celery import app
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import Subscribers, MenuItems
from django_backend_test.settings import WEBHOOK

 
@app.task
def mail_remainder(menu,link):
	items_menu = MenuItems.objects.filter(menu_id=menu.pk).values_list('name', flat=True)
	list_mail = Subscribers.objects.values_list('email', flat=True)
	subject,from_email,to = 'Menu of the Day','alertas@electroquimica.cl',list_mail
	html_content = render_to_string('menu_day.html',{'menu':items_menu,'link':str(link)})
	text_content = strip_tags(html_content)
	msg = EmailMultiAlternatives(subject,text_content,from_email,to)
	msg.attach_alternative(html_content,"text/html")
	msg.send()

@app.task
def slack_remainder(menu,link):
	msg = u"Hola!\nDejo el menú de hoy :)\n {0} <http://{1}>"
	items_menu= MenuItems.objects.filter(menu_id=menu.pk).values_list('name', flat=True)
	text="".join([x+"\n" for x in items_menu])
	data = {"text":msg.format(text,link), "username":"Nora", "icon_emoji": ":knife_fork_plate:",}
	headers = {'Content-type': 'application/json'}
	response = requests.post(WEBHOOK, data=json.dumps(data), headers=headers)