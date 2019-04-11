from django.shortcuts import render, redirect
from django.views.generic import ListView
from asynctask import *
from celery_app.settings import BASE_DIR
from .tasks import *
import requests
import logging
from django.http import *
# Create your views here.

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class AsyncTaskView(ListView):

    def get(self, request, **kwargs):
        try:
            if request.method == "GET":
                logging.info('Request received')
                '''
                Do something heavy.
                Calling task
                '''
                async_response = parallel_processing.delay() # declared in task.py

                if async_response:
                    logging.info('Async task response :' + str(async_response))
                    result = {'response': "Sit tight, process has started. For more details check console with process id %s" % async_response }
                else:
                    logging.info('Something went wrong with async process, for more details check logs.')
                    result = {'response': "Something went wrong with task threads, for more details check logs."}

                return HttpResponse(JsonResponse(result, safe=False), content_type='application/json')
        except Exception as ex:
            logging.exception('Exception causes by : ' + str(ex))
            result = {'response': "Exception causes by : " + str(ex)}
            return HttpResponse(JsonResponse(result, safe=False), content_type='application/json')