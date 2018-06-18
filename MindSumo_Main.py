#Thierno Diallo

from flask import Flask, render_template, request
import requests
import base64
import json

#--------------------------------------Helper methods to retrieve data with api--------------------------------------------------------------------------------------------------------------------------------------

def subscriptions(username,password):
    # username = input("Username: ")
    # password = input("Password: ")
    url = "https://gpodder.net/subscriptions/"+username.lower()+".json" #Get All Subscriptions api

    user_pass = username.lower()+":"+password.lower()
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
    return(subscription_list)


def search(search_string):
    # search_string = input("Search: ")
    url= "https://gpodder.net/search.json?q="+search_string.lower() #Podcast Search api

    response = requests.get(url)

    data = json.dumps(response.json())
    data = json.loads(data)

    search_result_list = []
    x=0
    for i in data:
        search_result_list.append("Title: "+data[x]['title']+" -- "+"Subscribers: "+str(data[x]['subscribers'])+" -- "+"Description: "+data[x]['description'])
        x += 1
    return (search_result_list)


def search_by_genre(genre_selection):
    genre_options = {"1":"Art", "2":"Comedy", "3":"Educational", "4":"Gaming", "5":"Music", "6":"News", "7":"Politics", "8":"Sci-Fi", "9":"Sports", "10":"Technology", "11":"Other Genre"} # a dictionary of the genre options corresponding with a number
    # print(genre_options)
    # genre_selection = input("Select Genre: #")

    url = "https://gpodder.net/api/2/tag/" + genre_selection.lower() + "/10.json" #Retrieve Podcasts for Tag api

    response = requests.get(url)
    data = json.dumps(response.json())
    data = json.loads(data)

    search_result_list = []
    x = 0
    for i in data:
        search_result_list.append("Title: " + data[x]['title'] + " -- " + "Subscribers: " + str(
            data[x]['subscribers']) + " -- " + "Description: " + data[x]['description'])
        x += 1
    return(search_result_list)


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
    return(result_list)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#*****************************************The build of the website is below***********************************************************************************************************************************

app = Flask(__name__)

posts = [                             #This list for the front page results (featured)
    {
        'title': search("ign")[0].split("--")[0],
        'subscriptions': search("ign")[0].split("--")[1],
        'content': search("ign")[0].split("--")[2],
    },
    {
        'title': search("cat")[0].split("--")[0],
        'subscriptions': search("cats")[0].split("--")[1],
        'content': search("cats")[0].split("--")[2],
    },
    {
        'title': search("music")[0].split("--")[0],
        'subscriptions': search("music")[0].split("--")[1],
        'content': search("music")[0].split("--")[2],
    }
]


results_popularity = []
x=0
for i in search_by_popularity():         #This for loop will create a result box and fill it with data for each item in the list, result_list
    results_popularity.append(
    {
        'title': search_by_popularity()[x].split("--")[0],
        'subscriptions': search_by_popularity()[x].split("--")[1],
        'content': search_by_popularity()[x].split("--")[2],
    }
    )
    x+=1


#Below are the website pages

@app.route("/")
@app.route("/home")
def home_web():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about_web():
    return render_template('about.html')


@app.route("/search", methods=['GET', 'POST'])
def search_web():
    if request.method == "POST":
        inquiry = request.form['inquiry']
        results_search = []
        x=0
        for i in search(inquiry):
            results_search.append(
            {
                'title': search(inquiry)[x].split("--")[0],
                'subscriptions': search(inquiry)[x].split("--")[1],
                'content': search(inquiry)[x].split("--")[2],
            }
            )
            x+=1
            # if results_search == []:
            #     return "No Result"

        return render_template('search2.html', inquiry=inquiry, results_search=results_search)

    return render_template('search.html')



@app.route("/subscriptions", methods=['GET', 'POST'])
def subscriptions_web():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        subscriptions_list = []
        x=0
        for i in subscriptions(username,password):            #The user's input for the username and password is taken and passed into the subscriptions function which returns a list of their subscriptions
            subscriptions_list.append(
            {
                'title': subscriptions(username,password)[x].split("--")[0],
                'subscriptions': subscriptions(username,password)[x].split("--")[1],
                'content': subscriptions(username,password)[x].split("--")[2],
            }
            )
            x+=1
            # if results_search == []:
            #     return "No Result"

        return render_template('subscriptions2.html', username=username, password=password, subscriptions_list=subscriptions_list)

    return render_template('subscriptions.html')



@app.route("/search_by_genre", methods=['GET', 'POST'])
def search_by_genre_web():
    genre = ""
    if request.method == "POST":
        if request.form['submit'] == 'Art':
            genre = "art"
        elif request.form['submit'] == 'Comedy':
            genre = "comedy"
        elif request.form['submit'] == 'Educational':
            genre = "Educational"
        elif request.form['submit'] == 'Gaming':
            genre = "Gaming"
        elif request.form['submit'] == 'Music':
            genre = "Music"
        elif request.form['submit'] == 'News':
            genre = "News"
        elif request.form['submit'] == 'Politics':
            genre = "Politics"
        elif request.form['submit'] == 'Sci-Fi':
            genre = "Sci-Fi"
        elif request.form['submit'] == 'Sports':
            genre = "Sports"
        elif request.form['submit'] == 'Technology':
            genre = "Technology"
        elif request.form['submit'] == 'Other':
            genre = "comedy"
        genre_inquiry = request.form['genre_inquiry']
        genre_results_search = []
        x=0
        for i in search_by_genre(genre):
            genre_results_search.append(
            {
                'title': search_by_genre(genre)[x].split("--")[0],
                'subscriptions': search_by_genre(genre)[x].split("--")[1],
                'content': search_by_genre(genre)[x].split("--")[2],
            }
            )
            x+=1
            # if results_search == []:
            #     return "No Result"

        return render_template('search_by_genre2.html', genre=genre, genre_results_search=genre_results_search)

    return render_template('search_by_genre.html')


@app.route("/search_by_popularity")
def search_by_popularity_web():
    return render_template('search_by_popularity.html', results_popularity=results_popularity)

@app.route("/smart_sort")
def smart_sort_web():
    return render_template('smart_sort.html')

@app.route("/suggestions")
def suggestions_web():
    return render_template('suggestions.html')

if __name__ == '__main__':
    app.run(debug=True)
