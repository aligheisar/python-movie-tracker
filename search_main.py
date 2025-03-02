import requests

url = "https://imdb146.p.rapidapi.com/v1/find/"

headers = {
	"X-RapidAPI-Key": "deebf3f8ebmsh1b68ea23f0ae3ebp1bdb76jsn1fc635b422be",
	"X-RapidAPI-Host": "imdb146.p.rapidapi.com"
}

# functions
def operation():
    while True:
        operation = input("What do you want to do? (1- search movie): ")
        if operation.isdigit():
            operation = int(operation)
            return operation
        else:
            print("Please enter a valid number.")

def response(movie_name):
    movie_name = {"query": movie_name}
    response = requests.get(url, headers=headers, params=movie_name)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.status_code)
        return

def search_movie():
    while True:
        movie_name = input("What is the name of the movie?: ")
        if movie_name:
            break
        else:
            print("Please enter a movie name.")
    data = response(movie_name)
    print(data)
    if data:
        title_results = data["titleResults"]["results"]
        for index, movie in enumerate(title_results):
            print("=========================================")
            print(f"{index + 1}. {movie['titleNameText']}")
            print(f"   release date: {movie['titleReleaseText']}")
            print(f"   type: {movie['titleTypeText']}")

operation = operation()
match operation:
    case 1:
        search_movie()