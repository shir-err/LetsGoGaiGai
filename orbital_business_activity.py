#pip install google-search-results
#pip install pyshorteners

import random
import pyshorteners
from serpapi import GoogleSearch

#API_Key
#api_key = "8b38a0a2de4c3f9ccbb19ec20b57605e14d373ad62df11723ec7c3ce73d44e93" #hl account
api_key = "1baa77a7fa374ed6e2ff1b831a0d37fe427f231c9ecb1e1e0a91a71ff8adf35b" #hl's sister account
#api_key = "3dfc85adf51ab0fce6034e5ea02c0e9cb3dd34a80fe2b32762d9e7c736b4990e" #shir er account

#shorten url
type_tiny = pyshorteners.Shortener()

#search for attractions
def attraction_api(index):
   search = GoogleSearch({
      "engine": "google",
      "q": "Singapore Attractions", 
      "location": "Singapore",
      "api_key": api_key
      })
   result = search.get_dict()
   attraction = result["top_sights"]["sights"][index]["title"]
   return attraction

#search for restaurant
def restaurant_lst(q):
   search = GoogleSearch({
      "engine": "google",
      "q": q, 
      "location": "Singapore",
      "api_key": api_key
      })
   result = search.get_dict()
   R1 = result["local_results"]["places"][0]["title"]
   R2 = result["local_results"]["places"][1]["title"]
   R3 = result["local_results"]["places"][2]["title"]
   lst = [R1, R2, R3]
   return lst

#search for adventure/food/others
def activity_lst(input):
   search = GoogleSearch({
      "engine": "google",
      "q": input, 
      "location": "Singapore",
      "api_key": api_key
      })
   result = search.get_dict()
   activity = result["inline_people_also_search_for"][random.randint(0, 1)]["items"]
   lst = []
   for dict in activity:
      lst.append(dict["name"])
   return lst


#image
def image_api(activity):
   search_image = GoogleSearch({
      "engine": "google_images",
      "q": activity + "in Singapore",
      "ijn": "0",
      "api_key": api_key
      })
   image_result = search_image.get_dict()
   img = image_result["images_results"][0]["original"]
   return img


#choosen
def choosen(activity):
   details = []
   search = GoogleSearch({
      "engine": "google",
      "q": activity + "in Singapore", 
      "location": "Singapore",
      "api_key": api_key
      })
   result = search.get_dict()
   try:
      desc = result["knowledge_graph"]["description"]
      map = type_tiny.tinyurl.short(result["knowledge_graph"]["local_map"]["link"])
   except:
      desc = result["organic_results"][0]["title"]
      lst = result["search_information"]["menu_items"]
      index = next((index for (index, d) in enumerate(lst) if d["title"] == "Maps"), None)
      map = type_tiny.tinyurl.short(result["search_information"]["menu_items"][index]["link"])
   link = type_tiny.tinyurl.short(result["organic_results"][0]["link"])
   details.append(desc)
   details.append(map)
   details.append(link)
   return details


#top3_options
def top3_options(activity):
   search = GoogleSearch({
   "engine": "google",
   "q": activity + "in Singapore", 
   "location": "Singapore",
   "api_key": api_key
   })
   result = search.get_dict()
   O1 = result["organic_results"][0]["title"]
   O1_link = type_tiny.tinyurl.short(result["organic_results"][0]["link"])
   O1_details = [O1, O1_link]
   O2 = result["organic_results"][1]["title"]
   O2_link = type_tiny.tinyurl.short(result["organic_results"][1]["link"])
   O2_details = [O2, O2_link]
   O3 = result["organic_results"][2]["title"]
   O3_link = type_tiny.tinyurl.short(result["organic_results"][2]["link"])
   O3_details = [O3, O3_link]
   details = [O1_details, O2_details, O3_details]
   return details
   
