
# Django Celery - With Parallel Processing

Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while 

providing operations with the tools required to maintain such a system.

It’s a task queue with focus on real-time processing, while also supporting task scheduling.


## Installing requirements

	$ pip install -r requirements.txt

## Using Celery with Django 

We will cover all these : 

	- Choosing and installing a message transport (broker).
	- Installing Celery and creating first task.
	- Starting the worker and calling tasks.
	- Keeping track of tasks as they transition through different states, and inspecting return values.


#### Choosing a Broker

Celery requires a solution to send and receive messages; usually this comes in the form of a separate service called a message broker.

There are several choices available, including:

	- RabbitMQ
	- Redis
	- Amazon SQS

Here we will use `redis` as a broker. For the Redis support you have to install additional dependencies. You can install both Celery and these dependencies in one go using the **celery[redis]** bundle.

	$ pip install -U "celery[redis]"

#### Installing Celery

Celery is on the Python Package Index (PyPI), so it can be installed with standard Python tools like **pip or easy_install** :

	$ pip install celery

#### Creating first task 

To use Celery with your Django project you must first define an instance of the Celery library (called an “app”)

1. The recommended way is to create a new `celery_app/celery_app/celery.py` module that defines the Celery instance.
 __file__: __celery_app/celery_app/celery.py__

 ~~~
 	from __future__ import absolute_import, unicode_literals
	import os
	from celery import Celery

	# set the default Django settings module for the 'celery' program.
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_app.settings')

	app = Celery('celery_app', backend='redis://localhost')

	# Using a string here means the worker doesn't have to serialize
	# the configuration object to child processes.
	# - namespace='CELERY' means all celery-related configuration keys
	#   should have a `CELERY_` prefix.
	app.config_from_object('django.conf:settings', namespace='CELERY')

	# Load task modules from all registered Django app configs.
	app.autodiscover_tasks()


	@app.task(bind=True)
	def debug_task(self):
	    print('Request: {0!r}'.format(self.request))
 ~~~

2. Then you need to import this app in your `celery_app/celery_app/__init__.py` module. This ensures that the app is loaded when Django starts:

 __file__ : __celery_app/celery_app/__init__.py__

~~~
	from __future__ import absolute_import, unicode_literals

	# This will make sure the app is always imported when
	# Django starts so that shared_task will use this app.
	from .celery import app as celery_app

	__all__ = ('celery_app',)
~~~

3. Let’s create the file `tasks.py`. Using the `@shared_task` decorator.

The tasks you will write probably live in reusable apps, and reusable apps cannot depend on the project itself, so you can also import your app instance directly.

The **@shared_task** decorator lets you create tasks without having any concrete app instance:

__file__ : __celery_app/asynctask/tasks.py__

~~~
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import eventlet
from eventlet.green.urllib import request as eventletrequest
from eventlet.green import socket
from eventlet.green import threading
from eventlet.green import asyncore
import logging
import requests

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

@shared_task
def parallel_processing():
	urls = [
		"https://sample-videos.com/zip/100mb.zip",
		"https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_30mb.mp4"
		"https://code9tech.com/",
		"http://kmmc.in/wp-content/uploads/2014/01/lesson2.pdf",
		"https://sample-videos.com/download-sample-zip.php",
		"http://www.google.com/intl/en_ALL/images/logo.gif",
		"https://www.python.org/static/img/python-logo.png",
		"http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
		"https://astrahospital.com/ortho/",
	]
	try:
		with eventlet.Timeout(10) as t:
			pool = eventlet.GreenPool(200)
			for url, body in pool.imap(fetch, urls):
				if t == 10:
					break
				logging.info("Body from url and length of data is : %s %s", str(url), str(body))
		return True
	except eventlet.Timeout as te:
		if te != t:
			logging.exception("Timeout exception : "+ str(t))

	except Exception as e:
		logging.exception("Exception occured : " + str(e))

def fetch(url):
	logging.info("Opening : " + str(url))
	body = requests.get(url)
	logging.info("done with : " + str(url))
	return url, body
~~~
__Brief about__ `task.py`  

Here I am crawling multiple websites at the same time in different threads, all these websites either containing heavy data or having long response time. Doing it so in the normal way will tedious task to do, best way to perform this type tasks asynchronously with the task queue system. I am creating here `Green thread` using `Eventlet`. 

Eventlet is built around the concept of green threads (i.e. coroutines, we use the terms interchangeably) that are launched to do network-related work. Green threads differ from normal threads.


4. Add the `CELERY_BROKER_URL` configuration to the `settings.py` file.

		CELERY_BROKER_URL = 'redis://localhost:6379/0'

5. Keeping Results & track of tasks

If you want to keep track of the tasks states, Celery needs to store or send the states somewhere. For that I am using redis. To result backend setup, go to  file __celery_app/celery_app/celery.py__.

		app = Celery('celery_app', backend='redis://localhost')

## Running the Celery worker server

	$ celery worker --app=celery_app -l info

	It looks like this:

![Celery worker window](https://github.com/vickymax/django-celery/blob/master/worker_console.png)

## Run Django app 
	
		$ python manage.py runserver 127.0.0.1:8000

The site instance should now be viewable at http://127.0.0.1:8000/async/task



## Django APP structure after Celery Setup

~~~
celery_app/
 |-- celery_app/
 |    |-- asynctask/
 |    |    |-- migrations/
 |    |    |-- __init__.py
 |    |    |-- admin.py
 |    |    |-- apps.py
 |    |    |-- models.py
 |    |    |-- tasks.py
 |    |    |-- tests.py
 |    |    |-- urls.py
 |    |    +-- views.py
 |    |-- __init__.py
 |    |-- celery.py
 |    |-- settings.py
 |    |-- urls.py
 |    +-- wsgi.py
 |-- .gitignore
 |-- db.sqlite3
 |-- manage.py
 |-- README.md
 +-- requirements.txt
 +-- worker_console.png

~~~

## Still look wrong? 

Contact the developer and tell me what you tried to do that didn’t work.

- [Reporting an issue](https://github.com/vickymax/django-celery/issues/new).
