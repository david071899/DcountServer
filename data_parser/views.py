# -*- coding: utf-8 -*-
from django.shortcuts import render
from data_parser.models import PostData, ParseError
from django.shortcuts import  render_to_response
from django.template import RequestContext

import requests
from bs4 import BeautifulSoup
# import multiprocessing
from threading import Thread, Lock
import time


def get_category():
  res = requests.get("https://www.dcard.tw/f")
  soup = BeautifulSoup(res.text, 'html.parser')
  target_tag = soup.find_all('a', class_ = "ForumEntry_link_3tNC4")

  category_list = []
  for i in target_tag:
    category_list.append(i["href"].split("/")[-1])

  category_list.remove('f')

  return category_list


# def get_start_id(category):
#   res = requests.get("https://www.dcard.tw/f/"+ category +"?latest=true")
#   soup = BeautifulSoup(res.text, 'html.parser')
#   try:
#     start_id = soup.find_all('a', class_ = "PostEntry_entry_2rsgm")[1]["href"].split('/')[-1]
#     return start_id
#   except:
#     pass

def parse_id(category):

  id_loop = ""


  while True:

    print id_loop

    try:
      res = requests.get("https://www.dcard.tw/_api/forums/"+ category +"/posts?popular=false" + str(id_loop))

      if res.json() != []:
        id_loop = "&before=" + str(res.json()[-1]["id"])
      elif res.json() == []:
       break

    except Exception,e:

      print str(e)

      break
    
    #create row data
    for post in res.json():
      try:
        
        PostData.objects.update_or_create(
          id = post["id"],
          title = post["title"],
          gender = post["gender"],
          like_count = post["likeCount"],
          comment_count = post["commentCount"],
          created_at = post["createdAt"],
          forum_alias = post["forumAlias"],
          forum_name = post["forumName"]
        )

      except Exception,e:

        ParseError.objects.create(
          id = post["id"],
          content = str(e)
        )

        continue


# def parse_content_func(category):

#   print category
  
#   for post in PostData.objects.filter(forum_alias = category):
#       res = requests.get("https://www.dcard.tw/_api/posts/"+ str(post.id)).json()

#       post.title = res["title"]
#       post.gender = res["gender"]
#       post.created_at = res["createdAt"]
#       post.like_count = res["likeCount"]
#       post.comment_count = res["commentCount"]
#       post.content = res["content"]

#       print str(post.id) + "parse content"

#       post.save()



# def parse_content(category_list):

#   content_workers = []
#   for category in category_list:
#     worker = Thread(target = parse_content_func, args = (category, ))
#     content_workers.append(worker)
#     worker.start()

#   for worker in content_workers:
#     worker.join()

  


def index(request):
  category_list = get_category()
  
  workers = []

  tStart = time.time()

  for i in category_list:
    
    worker = Thread(target = parse_id, args = (i, ))
    workers.append(worker)
    worker.start()

    
  for worker in workers:
    worker.join()
  
  # parse_content(category_list)

  tEnd = time.time()
  spent_time = tEnd - tStart

  return render_to_response('index.html',RequestContext(request,locals()))


# def get_end_id():
#   res = requests.get("https://www.dcard.tw/f?latest=true")
#   soup = BeautifulSoup(res.text, 'html.parser')
#   try:
#     start_id = soup.find_all('a', class_ = "PostEntry_entry_2rsgm")[0]["href"].split('/')[-1]
#     return start_id
#   except:
#     pass

# def myrange(start_id, end_id):
#   x = start_id
#   while True:
#     yield x
#     x += 1  
#     if x == end_id:
#       break


# def parse(post_id):
#   while True:
    
#     res = requests.get("https://www.dcard.tw/_api/posts/" + str(next(post_id))).json()

#     if len(res) > 3:

#       PostData.objects.get_or_create(
#         id = res["id"],
#         created_at = res["createdAt"],
#         forum_alias = res["forumAlias"],
#         forum_name = res["forumName"],
#         title = res["title"],
#         gender = res["gender"],
#         like_count = res["likeCount"],
#         comment_count = res["commentCount"],
#         content = res["content"]
#       )
      
#       print res["title"]

#     else:
#       print "id not available"

# def index(request):

#   tStart = time.time()
  
#   end_id = get_end_id()  
#   post_id_generator = myrange(10001, int(end_id))

#   workers = []
#   for i in xrange(50):
#     worker = Thread(target = parse, args = (post_id_generator, ))
#     workers.append(worker)
#     worker.start()

#   for worker in workers:
#     worker.join()


#   tEnd = time.time()
#   spent_time = tEnd - tStart

#   return render_to_response('index.html',RequestContext(request,locals()))















