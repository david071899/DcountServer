# -*- coding: utf-8 -*-
from django.shortcuts import render
from data_parser.models import PostData, ParseError
from django.shortcuts import  render_to_response
from django.template import RequestContext

from parser_method.parse_all_content import start_parse_content
from parser_method.parse_all_post import start_parse_post

import requests
from bs4 import BeautifulSoup
import random
from threading import Thread, Lock
import time

def parse_all_post(request):

  tStart = time.time()

  start_parse_post()

  tEnd = time.time()

  spent_time = tEnd - tStart

  return render_to_response('index.html',RequestContext(request,locals()))

def parse_all_content(request):

  tStart = time.time()

  start_parse_content()

  tEnd = time.time()

  spent_time = tEnd - tStart

  return render_to_response('index.html',RequestContext(request,locals()))












