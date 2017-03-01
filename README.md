# backend-test
A technical test to apply for a job

## Table of Contents

- [Config](#config)

## Config

To run this project you need to add some variables to the settings file.

- [Dependencies](#dependencies)
- [Slack](#webhook)
- [Mail Settings](#mail)

## Dependencies
This project uses async process to send messages by email or slack. To achieve this, we use celery and rabbitmq.
To use this project you need to setup a celery enviroment with rabbitmq as broker. Additionally you need to install django-celery and add in your installed apps settings.
To this project, we use celery 3.1.

You can get more information in:
http://docs.celeryproject.org/en/3.1/django/index.html
https://www.rabbitmq.com/

## Slack
To send messages to slack channel, you need to set a Webhook variable.
You can get a webhook in https://api.slack.com/incoming-webhooks

## Mail Settings
To send a remainder by mail, you need to set the email variables in the settings file.
