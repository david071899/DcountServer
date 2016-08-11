# coding=UTF-8

import requests
from bs4 import BeautifulSoup
from threading import Thread
import multiprocessing


def myrange(start_id, end_id):
  x = start_id
  while True:
    yield x
    x += 1  
    if x == end_id:
      break

def parse(post_id):
  while True:
    
    res = requests.get("https://www.dcard.tw/_api/posts/" + str(next(post_id))).json()

    if len(res) > 3:
      print res["title"]
    else:
      print "id not available"

if __name__ == '__main__':
  post_id_generator = myrange(10001, 224525403)

  for i in xrange(20):
    worker = Thread(target = parse, args = (post_id_generator, ))
    worker.start()





# if __name__ == '__main__':
#   pool = multiprocessing.Pool(processes = 4) #use all available cores, otherwise specify the number you want as an argument
#   for i in xrange(10001, 224525403):
#       pool.apply_async(parse, args=(i,))
#   pool.close()
#   pool.join()
  


# def get_category():
#   res = requests.get("https://www.dcard.tw/f")
#   soup = BeautifulSoup(res.text, 'html.parser')
#   target_tag = soup.find_all('a', class_ = "ForumEntry_link_3tNC4")

#   category_list = []
#   for i in target_tag:
#     category_list.append(i["href"].split("/")[-1])

#   category_list.remove('f')

#   return category_list


# def get_start_id(category):
#   res = requests.get("https://www.dcard.tw/f/"+ category +"?latest=true")
#   soup = BeautifulSoup(res.text, 'html.parser')
#   start_id = soup.find_all('a', class_ = "PostEntry_entry_2rsgm")[-1]["href"].split('/')[-1]
#   return start_id

# def parser(category, start_id):

#   id_loop = start_id

#   print category
#   while True:
#     print id_loop
#     try:
#       res = requests.get("https://www.dcard.tw/_api/forums/"+ category +"/posts?popular=false&before=" + str(id_loop))
#       id_loop = res.json()[-1]["id"]
#     except:
#       print "all ids are already get"
#       break

# if __name__ == "__main__":
#   category_list = get_category()

#   for i in category_list:
#     start_id = get_start_id(i)
#     parser(i, start_id)