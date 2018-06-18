#Thierno Diallo

import requests
import base64
import json


def subscriptions(username,password):
    username = input("Username: ")
    password = input("Password: ")
    url = "https://gpodder.net/subscriptions/"+username+".json" #Get All Subscriptions api

    user_pass = username+":"+password
    encoded = base64.b64encode(user_pass.encode()) #encodes the username and password

    headers = {'Authorization': 'Basic '+str(encoded)[2:]} #gives us the login token we need

    response = requests.get(url, headers=headers) #retrieves user subscriptions with their login token

    data = json.dumps(response.json())
    data = json.loads(data) #turns json format into Python friendly format

    subscription_list = []
    x=0
    for i in data:
        subscription_list.append("Title: "+data[x]['title']+" -- "+"Subscribers: "+str(data[x]['subscribers'])+" -- "+"Description: "+data[x]['description']) #takes the useful data (title, subscribers, and description) and puts it neatly in a list
        x+=1
    print(subscription_list)

subscriptions(username="", password="")

def search(search_string):
    search_string = input("Search: ")
    url= "https://gpodder.net/search.json?q="+search_string #Podcast Search api

    response = requests.get(url)

    data = json.dumps(response.json())
    data = json.loads(data)

    search_result_list = []
    x=0
    for i in data:
        search_result_list.append("Title: "+data[x]['title']+" -- "+"Subscribers: "+str(data[x]['subscribers'])+" -- "+"Description: "+data[x]['description'])
        x += 1
    print (search_result_list)

# search(search_string="")

def search_by_genre(genre_selection):
    genre_options = {"1":"Art", "2":"Comedy", "3":"Educational", "4":"Gaming", "5":"Music", "6":"News", "7":"Politics", "8":"Sci-Fi", "9":"Sports", "10":"Technology", "11":"Other Genre"} # a dictionary of the genre options corresponding with a number
    print(genre_options)
    genre_selection = input("Select Genre: #")

    if genre_selection == "11":
        genre = input("Type in Genre: ")
        url = "https://gpodder.net/api/2/tag/" + genre.lower() + "/10.json" #Retrieve Podcasts for Tag api
    else:
        genre = genre_options.get(genre_selection)
        url = "https://gpodder.net/api/2/tag/" + genre.lower() + "/10.json" #Retrieve Podcasts for Tag api

    response = requests.get(url)
    data = json.dumps(response.json())
    data = json.loads(data)

    search_result_list = []
    x = 0
    for i in data:
        search_result_list.append("Title: " + data[x]['title'] + " -- " + "Subscribers: " + str(
            data[x]['subscribers']) + " -- " + "Description: " + data[x]['description'])
        x += 1
    print(search_result_list)

# search_by_genre(genre_selection="")

def search_by_popularity():
    url = "https://gpodder.net/toplist/10.json" #Podcast Toplist api

    response = requests.get(url)

    data = json.dumps(response.json())
    data = json.loads(data)

    result_list = []
    x = 0
    for i in data:
        result_list.append("Title: " + data[x]['title'] + " -- " + "Subscribers: " + str(
            data[x]['subscribers']) + " -- " + "Description: " + data[x]['description'])
        x += 1
    print(result_list)

# search_by_popularity()



# episode_url = "http%3A%2F%2Fcontent.sixgun.org%2Flinuxoutlaws370a.mp3"
# podcast_url = "http%3A%2F%2Ffeeds.feedburner.com%2Flinuxoutlaws"
# url = "https://gpodder.net/api/2/data/episode.json?url="+episode_url+"?&podcast="+podcast_url
#
# response = requests.get(url)
#
# data = json.dumps(response.json())
# data = json.loads(data)
#
# print(response.json())

