# Create your tasks here
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
		"http://www.google.com/intl/en_ALL/images/logo.gif",
		"https://www.python.org/static/img/python-logo.png",
		"http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
		"https://astrahospital.com/ortho/",
		"https://code9tech.com/",
		"http://kmmc.in/wp-content/uploads/2014/01/lesson2.pdf",
		"https://sample-videos.com/download-sample-zip.php",
		"https://sample-videos.com/zip/100mb.zip",
		"https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_30mb.mp4"
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