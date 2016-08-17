# coding=UTF-8

import requests
from bs4 import BeautifulSoup
from threading import Thread
import multiprocessing
import psycopg2

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
#       print res["title"]
#     else:
#       print "id not available"

# if __name__ == '__main__':
#   post_id_generator = myrange(10001, 224525403)

#   for i in xrange(20):
#     worker = Thread(target = parse, args = (post_id_generator, ))
#     worker.start()


# if __name__ == '__main__':
#   pool = multiprocessing.Pool(processes = 4) #use all available cores, otherwise specify the number you want as an argument
#   for i in xrange(10001, 224525403):
#       pool.apply_async(parse, args=(i,))
#   pool.close()
#   pool.join()
  


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
#   start_id = soup.find_all('a', class_ = "PostEntry_entry_2rsgm")[-1]["href"].split('/')[-1]
#   return start_id


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

        if post["anonymousSchool"]:
          cur.execute(
            """
            INSERT INTO data_parser_postdata 
            (id, title, gender, like_count, comment_count, 
            created_at, forum_alias, forum_name, school_name, content)
            VALUES
            (%d, %s, %s, %d, %d, %s, %s, %s, %s, %s)
            """ %
            (post["id"], post["title"], post["gender"], post["likeCount"], post["commentCount"],
              str(post["createdAt"]), post["forumAlias"], post["forumName"], "anonymous", ""
            )
          )

          # PostData.objects.update_or_create(
          #   id = post["id"],
          #   default = {
          #   'title': post["title"],
          #   'gender': post["gender"],
          #   'like_count': post["likeCount"],
          #   'comment_count': post["commentCount"],
          #   'created_at': post["createdAt"],
          #   'forum_alias': post["forumAlias"],
          #   'forum_name': post["forumName"],
          #   'school_name': "anonymous"
          # })
        else:
          cur.execute(
            """
            INSERT INTO data_parser_postdata 
            (id, title, gender, like_count, comment_count, 
            created_at, forum_alias, forum_name, school_name, content)
            VALUES
            (%d, %s, %s, %d, %d, %s, %s, %s, %s, %s)
            """ % 
            (post["id"], post["title"], post["gender"], post["likeCount"], post["commentCount"],
              str(post["createdAt"]), post["forumAlias"], post["forumName"], post["school"], ""
            )
          )

          # PostData.objects.update_or_create(
          #   id = post["id"],
          #   default = {
          #   'title': post["title"],
          #   'gender': post["gender"],
          #   'like_count': post["likeCount"],
          #   'comment_count': post["commentCount"],
          #   'created_at': post["createdAt"],
          #   'forum_alias': post["forumAlias"],
          #   'forum_name': post["forumName"],
          #   'school_name': post["school"]
          # })

      except Exception,e:

        print str(e)
        continue

if __name__ == "__main__":

  conn =  psycopg2.connect("dbname=dcount user=davy")

  cur = conn.cursor()

  category_list = get_category()

  print category_list

  category_list = reversed(category_list)

  workers = []

  for category in category_list:
    worker = Thread(target = parse_id, args = (category, ))
    workers.append(worker)
    worker.start()
    worker.join() 

  conn.commit()
    
  # for worker in workers:
  #   worker.join()

