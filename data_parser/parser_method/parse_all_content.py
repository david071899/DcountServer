from data_parser.models import PostData, ParseError

import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock
import time

def get_all_category():
  res = requests.get("https://www.dcard.tw/f", headers = { 'Connection':'close' })
  soup = BeautifulSoup(res.text, 'html.parser')
  target_tag = soup.find_all('a', class_ = "ForumEntry_link_3tNC4")

  category_list = []
  for i in target_tag:
    category_list.append(i["href"].split("/")[-1])

  category_list.remove('f')

  return category_list
  

def category_generator():
  category_list = get_all_category()
  for category in category_list:
    yield category

def parse_all_content(generator, sleep_sec):
  
  print sleep_sec
  
  time.sleep(sleep_sec)

  while True:

    try:
      category = generator.next()
      print category

    except Exception,e:
      break

    for post in PostData.objects.filter(forum_alias = category).filter(content = ''):
      print post.id
      try:
        res = requests.get("https://www.dcard.tw/_api/posts/" + str(post.id), headers = { 'Connection':'close' }).json()

        try:
          post.content = res["content"]
        except:
          pass

      except Exception,e:
        print str(e)

        continue

      post.save()


def start_parse_content():

  print "new parse content"

  generator = category_generator()

  workers = []

  for i in range(5):
    worker = Thread(target = parse_all_content, args = (generator, i, ))
    workers.append(worker)
    worker.start()

  for worker in workers:
    worker.join()
  
