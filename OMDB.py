import requests

api_key = "713bae62"
movie_name = input("Enter the movie title: ")
movie_id_number = input("Enter the movie imdb id number: ")
title_url = f"http://www.omdbapi.com/?t={movie_name}&plot=short&type={""}&apikey={api_key}"
imdb_url = f"http://www.omdbapi.com/?i=tt{movie_id_number}&plot=short&type={""}&apikey={api_key}"
response = requests.get(title_url)
data = response.json()
print(data)