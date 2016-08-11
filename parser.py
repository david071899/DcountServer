# coding=UTF-8
import requests
from bs4 import BeautifulSoup


res = requests.get("https://www.dcard.tw/f")

soup = BeautifulSoup(res.text, 'html.parser')

# target_tag = soup.find(class_ = "ForumEntryGroup_group_1WhBu").find_all(class_ = "ForumEntryGroup_group_1WhBu")

for tag in soup.select(".ForumList_list_3jlAj .ForumEntryGroup_group_1WhBu.ForumEntryGroup_groupExpanded_OQm_W .ForumEntry_link_3tNC4"):
  print tag["href"]


