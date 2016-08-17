import psycopg2
import requests
from bs4 import BeautifulSoup
from threading import Thread

conn_data_base =  psycopg2.connect("dbname=dcount user=davy")

cur = conn_data_base.cursor()

# cur.execute("SELECT * FROM data_parser_postdata WHERE forum_alias = 'bg';")

# print cur.fetchall()