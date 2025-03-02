import json
import datetime
from datetime import datetime as dt
import uuid
import time

def load_database(database_name):
    try:
        with open(f"{database_name}.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        data = []
    return data

def update_database(database_name, new_data):
    existing_data = load_database(database_name)
    existing_data.append(new_data)
    with open(f"{database_name}.json", 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4)

def replace_database(database_name, data):
    with open(f"{database_name}.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def sort_database(database_name):
    global field
    global reverse
    def custom_sort(data):
        if database_name == "movies":
            movie_id = list(data.keys())[0]
            movie_info = data[movie_id]
            if field not in movie_info:
                print(f"Field '{field}' not found in movie data.")
                return float('-inf') if reverse else float('inf')
            value = movie_info.get(field, None)
        else:
            value = data.get(field, None)

        if value is None and field in ["genre", "language", "country", "summery"]:
            return "0000000000000000" if reverse else "zzzzzzzzzzzzzzzzzzz"
        elif field == "type":
            order = {"movie": 1, "series": 2}
            return order.get(value, 0)
        elif value and field == "rate":
            order = {"terrible": 1, "not bad": 2, "good": 3, "great": 4, "legend": 5}
            return order.get(value, 0)
        elif field == "have seen":
            order = {"No": 1, "Half": 2, "Yes": 3}
            return order.get(value, 0)
        elif field in ["date added", "date updated"]:
            return dt.strptime(value, "%Y-%m-%d %H:%M:%S")
        elif value is None and field in ["release year", "imdb", "rate"]:
            return float('-inf') if reverse else float('inf')
        elif isinstance(value, (int, float)):
            return value
        else:
            return str(value).lower()
    def reverse_input():
        global reverse
        while True:
            reverse_input = input("Would you like to reverse the order? (y/n): ").strip().lower()
            if not reverse_input:
                reverse = False
                break
            match reverse_input:
                case "y":
                    reverse = True
                case "n":
                    reverse = False
                case _:
                    print("Please enter 'y' or 'n'")
                    time.sleep(.5)
                    continue
            break
        return reverse
    data = load_database(database_name)
    if not data:
        print(f"No data found in '{database_name}'")
        return
    if database_name == "movies":
        while True:
            print("1-Name")
            print("2-Release year")
            print("3-Genre")
            print("4-Language")
            print("5-Country")
            print("6-Type")
            print("7-imdb")
            print("8-Summery")
            print("9-Rate")
            print("10-Have seen")
            print("11-Date added")
            field_input = input("Select a field to Sort: ").strip()
            if not field_input:
                return
            if not field_input.isdigit():
                print("Please enter a number")
                time.sleep(.5)
                continue
            field_input = int(field_input)
            match field_input:
                case 1:
                    field = "name"
                case 2:
                    field = "release year"
                case 3:
                    field = "genre"
                case 4:
                    field = "language"
                case 5:
                    field = "country"
                case 6:
                    field = "type"
                case 7:
                    field = "imdb"
                case 8:
                    field = "summery"
                case 9:
                    field = "rate"
                case 10:
                    field = "have seen"
                case 11:
                    field = "date added"
                case _:
                    print("Please enter a number between 1 and 11")
                    time.sleep(.5)
                    continue
            reverse = reverse_input()
            break

        if field in ["release year", "imdb", "have seen", "rate", "date added"]:
            reverse = not reverse
    elif database_name == "collections":
        while True:
            print("1-Name")
            print("2-Date added")
            print("3-Date updated")
            field_input = input("Select a field to Sort: ")
            if not field_input:
                return
            if not field_input.isdigit():
                print("Please enter a number")
                time.sleep(.5)
                continue
            field_input = int(field_input)
            match field_input:
                case 1:
                    field = "name"
                case 2:
                    field = "date added"
                case 3:
                    field = "date updated"
                case _:
                    print("Please enter a number between 1 and 3")
                    time.sleep(.5)
                    continue
            reverse = reverse_input()
            break
        if field in ["date added", "date updated"]:
            reverse = not reverse
    else:
        print(f"Unsupported database name: {database_name}")
        return
    sorted_data = sorted(data, key=custom_sort, reverse=reverse)
    if not data == sorted_data:
        replace_database(database_name, sorted_data)
        print(f"{database_name} has been sorted successfully.")
    else:
        print("Sorted data has not changed.")

def search_database(database_name=None):
    global field
    global value
    founded_movies = []
    founded_collections = []
    if database_name is None:
        while True:
            print("1-Name")
            print("2-Date added")
            field_input = input("Select a field to search: ").strip()
            if not field_input:
                return
            if not field_input.isdigit():
                print("Please enter a number.")
                time.sleep(.5)
                continue
            field_input = int(field_input)
            match field_input:
                case 1:
                    field = "name"
                    break
                case 2:
                    field = "date added"
                case _:
                    print("Please enter 1 or 2.")
                    time.sleep(.5)
                    continue
            break
        if field == "name":
            value = name_input(all_keyword=False)
        else:
            value = input(f"Enter {field} value: ")
        if value:
            value = value.strip().lower()
        else:
            return
        movies = load_database("movies")
        collections = load_database("collections")
        for movie in movies:
            movie_id = list(movie.keys())[0]
            movie_info = movie[movie_id]
            if field == "date added":
                if value in movie_info[field]:
                    founded_movies.append(movie_id)
            else:
                if value == movie_info[field].lower():
                    founded_movies.append(movie_id)
        for col in collections:
            if field == "date added":
                if value in col[field]:
                    founded_collections.append(col["name"])
            else:
                if value == col[field].lower():
                    founded_collections.append(col["name"])
        founded_movies = list(set(founded_movies))
        founded_collections = list(set(founded_collections))
        if founded_movies:
            print("-----founded movies-----")
            print_movie_by_id(founded_movies)
        else:
            print("No movies found.")
        if founded_collections:
            print("-----founded collections-----")
            print_collection_by_name(founded_collections)
        else:
            print("No collections found.")
    if database_name == "movies":
        while True:
            print("1-Name")
            print("2-Release Year")
            print("3-Genre")
            print("4-Language")
            print("5-Country")
            print("6-Type")
            print("7-imdb")
            print("8-Summery")
            print("9-Rate")
            print("10-Have seen")
            print("11-Date added")
            field_input = input("Select a field to search: ").strip()
            if not field_input:
                return
            if not field_input.isdigit():
                print("Please enter a number.")
                time.sleep(.5)
                continue
            field_input = int(field_input)
            match field_input:
                case 1:
                    field = "name"
                    value = name_input(all_keyword=True).lower()
                case 2:
                    field = "release year"
                    value = release_year_input()
                case 3:
                    field = "genre"
                    value = multi_string_input("genre", join_char=False).lower()
                case 4:
                    field = "language"
                    value = multi_string_input("language", join_char=False).lower()
                case 5:
                    field = "country"
                    value = multi_string_input("country", join_char=False).lower()
                case 6:
                    field = "type"
                    value = type_input(required=False)
                case 7:
                    field = "imdb"
                    value = imdb_input()
                case 8:
                    field = "summery"
                    value = summary_input().lower()
                case 9:
                    field = "rate"
                    value = rate_input()
                case 10:
                    field = "have seen"
                    value = have_seen_input()
                case 11:
                    field = "date added"
                    value = input("Enter date added: ").strip()
                case _:
                    print("Please enter number between 1 and 11.")
                    time.sleep(.5)
                    continue
            if not value:
                return
            movies = load_database("movies")
            for movie in movies:
                movie_id = list(movie.keys())[0]
                movie_info = movie[movie_id]
                if field in ["name", "genre", "language", "country", "summery"]:
                    target_value = movie_info[field].lower()
                else:
                    target_value = movie_info[field]
                if field in ["summery", "date added"]:
                    if value in target_value:
                        founded_movies.append(movie_id)
                elif field in ["genre", "language", "country"]:
                    for val in field.lower():
                        if val in target_value:
                            founded_movies.append(movie_id)
                else:
                    if value == target_value:
                        founded_movies.append(movie_id)
            break
        founded_movies = list(set(founded_movies))
        if founded_movies:
            print("-----founded movies-----")
            print_movie_by_id(founded_movies)
        else:
            print("No movies found.")
    if database_name == "collections":
        while True:
            print("1-Name")
            print("2-Date added")
            print("3-Date updated")
            field_input = input("Select a field to search: ").strip()
            if not field_input:
                return
            if not field_input.isdigit():
                print("Please enter a number.")
                time.sleep(.5)
                continue
            field_input = int(field_input)
            match field_input:
                case 1:
                    field = "name"
                    value = name_input("Collection", all_keyword=True).lower()
                case 2:
                    field = "date added"
                    value = input("Enter date added: ").strip()
                case 3:
                    field = "date updated"
                    value = input("Enter date updated: ").strip()
                case _:
                    print("Please enter number between 1 and 3.")
                    time.sleep(.5)
                    continue
            if not value:
                return
            collections = load_database("collections")
            for collection in collections:
                if field == "name":
                    if value == collection[field].lower():
                        founded_collections.append(collection["name"])
                else:
                    if value in collection[field]:
                        founded_collections.append(collection["name"])
            break
        founded_collections = list(set(founded_collections))
        if founded_collections:
            print("-----founded collections-----")
            print_collection_by_name(founded_collections)
        else:
            print("No collections found.")

def search_select_movie(movies, allow_multiple_movies=True):
    movie_name = name_input()
    if not movie_name:
        return
    if movie_name.lower() == "/all":
        return 1.5
    found_movies = [
        list(movie.keys())[0] for movie in movies
        if movie_name.lower() == movie[list(movie.keys())[0]]["name"].lower()
    ]
    if not found_movies:
        print("Movie not found")
        time.sleep(.5)
        return
    if len(found_movies) > 1:
        print_movie_by_id(found_movies)
        selected_indices = ask_for_select(len(found_movies), False, allow_multiple_movies)
        if not selected_indices:
            return
        if isinstance(selected_indices, int):
            selected_movies = [found_movies[selected_indices - 1]]
        else:
            selected_movies = [found_movies[i - 1] for i in selected_indices]
        if allow_multiple_movies:
            return selected_movies
        else:
            return selected_movies[0]
    if allow_multiple_movies:
        return found_movies
    else:
        return found_movies[0]

def print_movie_details(index, movie):
    print(f"{index}:")
    for key, value in movie.items():
        print(f"    {key.capitalize()}: {"N/A" if value is None else value}")

def print_movie_by_id(movies_ids, gap=""):
    movies = load_database("movies")
    for index, movies_id in enumerate(movies_ids):
        for movie in movies:
            if movies_id in movie:
                movie_details = movie[movies_id]
                print(f"{gap}{index + 1}:")
                for key, value in movie_details.items():
                    print(f"{gap}    {key.capitalize()}: {"N/A" if value is None else value}")

def print_movie_items(selected_movie_id):
    global s_movie
    movies = load_database("movies")
    for index, movie in enumerate(movies):
        if selected_movie_id == list(movie.items())[0][0]:
            s_movie = movie[selected_movie_id]
    movie_detail = s_movie
    print(movie_detail["name"])
    del movie_detail["date added"]
    del movie_detail["img url"]
    counter = 0
    for key, value in movie_detail.items():
        counter += 1
        print(f"{counter}. {key.capitalize()}: {"N/A" if value is None else value}")
    return counter

def print_collection(index, collection):
    movies = load_database("movies")
    print(f"{index}. {collection["name"]}:")
    print(f"   Date added: {collection["date added"]}")
    print(f"   Date updated: {collection["date updated"]}")
    found_movie_id = [list(movie.keys())[0] for movie in movies if list(movie.keys())[0] in collection["items"]]
    print_movie_by_id(found_movie_id, "   ")

def print_collection_by_name(collection_names):
    movies = load_database("movies")
    collections = load_database("collections")
    for index, col_name in enumerate(collection_names):
        for collection in collections:
            if collection["name"] == col_name:
                print(f"{index + 1}. {collection["name"]}:")
                print(f"   Date added: {collection["date added"]}")
                print(f"   Date updated: {collection["date updated"]}")
                found_movie_id = []
                for movie in movies:
                    if list(movie.keys())[0] in collection["items"]:
                        found_movie_id.append(list(movie.keys())[0])
                print_movie_by_id(found_movie_id, "   ")


def check_movie_exist(movies, new_movie):
    new_movie_details = list(new_movie.values())[0]
    for existing_movie in movies:
        existing_movie_details = list(existing_movie.values())[0]
        if all(
            existing_movie_details.get(key) == new_movie_details.get(key)
            for key in ["name", "release year", "type"]
        ):
            return True
    return False

def ask_for_select(options, required=False, allow_multiple_movies=True):
    while True:
        user_input = input("Enter your choice: ").strip()
        if not user_input:
            if required:
                print("Please enter your choice.")
                continue
            else:
                return
        if user_input.lower() == "/all":
            return 1.5
        user_input_list = user_input.split(",")
        user_input_clean = []
        valid_input = True
        for each_selection in user_input_list:
            each_selection = each_selection.strip()
            if not each_selection:
                continue
            if each_selection.isdigit():
                user_input_clean.append(int(each_selection))
            else:
                print("Please enter valid numbers.")
                valid_input = False
                break
        if not valid_input:
            continue
        if not allow_multiple_movies and len(user_input_clean) > 1:
            print("Please enter only one movie.")
            continue
        if not user_input_clean:
            print("Please select at least one option.")
            continue
        if all(1 <= selection <= options for selection in user_input_clean):
            if len(user_input_clean) == 1:
                return user_input_clean
            return user_input_clean
        else:
            if options == 1:
                print("you can only input 1 for continue")
                continue
            print(f"Input must be between 1 and {options}.")
            continue

def is_float(input_value):
    try:
        float(input_value)
        return True
    except ValueError:
        return False


# inputs
def name_input(name="movie", required=False, all_keyword=False):
    while True:
        input_name = input(f"Enter {name} name: ").strip()
        if all_keyword:
            if input_name.lower() == "/all":
                print("You can't use this word")
                time.sleep(.5)
                continue
        if required and not input_name:
            print(f"Please enter {name} name")
        elif not required and not input_name:
            return
        else:
            return input_name

def release_year_input(name="movie", required=False):
    while True:
        year = input(f"Enter {name} release year: ").strip()
        if required and not year:
            print(f"Please enter {name} release year")
        elif not required and not year:
            return
        else:
            if year.isdigit() and len(year) == 4:
                year = int(year)
                if year <= datetime.datetime.now().year:
                    return year
                else:
                    print("Release year cannot be in the future")
            else:
                print("Please enter a valid 4-digit year")

def multi_string_input(use_for="", name="movie", required=False, join_char=True):
    values = []
    while True:
        value = input(f"Enter {name} {use_for}: ").strip()
        if required and not values and not value:
            print(f"Please enter {name} {use_for}")
        elif not required and not value:
            break
        else:
            values.append(value)
    if not values:
        return
    if join_char:
        return ", ".join(values)
    else:
        return values

def type_input(name="movie", required=False):
    while True:
        type_str = input(f"Enter {name} type (1-movie, 2-series): ").strip()
        if required and not type_str:
            print(f"Please enter {name} type")
        elif not required and not type_str:
            return
        else:
            if type_str.isdigit() and 1 <= int(type_str) <= 2:
                return ["movie", "series"][int(type_str) - 1]
            else:
                print("Please enter 1 or 2")

def imdb_input(name="movie", required=False):
    while True:
        imdb = input(f"Enter {name} imdb rate: ").strip()
        if required and not imdb:
            print(f"Please enter {name} imdb rate")
        elif not required and not imdb:
            return
        else:
            try:
                imdb = float(imdb)
                if 0 <= imdb <= 10:
                    return imdb
                else:
                    print("Please enter a number between 0 and 10")
            except ValueError:
                print("Please enter a valid number")

def summary_input(name="movie", required=False):
    while True:
        summary = input(f"Enter {name} summary: ").strip()
        if required and not summary:
            print(f"Please enter {name} summary")
        elif not required and not summary:
            return
        else:
            return summary

def rate_input(name="movie", required=False):
    while True:
        rate_str = input("Enter movie rate (1-terrible, 2-not bad, 3-good, 4-great, 5-legend): ").strip()
        if required and not rate_str:
            print(f"Please enter {name} rate")
        elif not required and not rate_str:
            return None
        else:
            if rate_str.isdigit() and 1 <= int(rate_str) <= 5:
                return ["terrible", "not bad", "good", "great", "legend"][int(rate_str) - 1]
            else:
                print("Please enter a number between 1 and 5")

def have_seen_input(required=False):
    while True:
        response = input("Have you seen this movie? (Y/N/H): ").strip().upper()
        if response in ["Y", "N", "H"]:
            return {"Y": "Yes", "N": "No", "H": "Half"}[response]
        elif not required:
            return
        print("Please enter Y, N, or H")


# collection
def add_collection():
    while True:
        name = name_input("collection", all_keyword=True)
        if not name:
            return
        collections = load_database("collections")
        if any(col["name"] == name for col in collections):
            print("Collection already exists.")
            continue
        collection = {
            "name": name,
            "date added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": []
        }
        update_database("collections", collection)
        print("Collection added successfully.")
        time.sleep(.5)
        return

def remove_collection():
    collections = load_database("collections")
    if not collections:
        print("You dont have any collection.")
        time.sleep(.5)
        return
    name = name_input("Collection")
    if not name:
        return
    if name == "/all":
        while True:
            check_answer = input("Are you sure you want to remove all collections? (Y/N): ").strip().upper()
            if check_answer == "Y":
                collections = []
                replace_database("collections", collections)
                print("Collections removed successfully.")
                time.sleep(.5)
                return
            elif check_answer == "N":
                return
    for index, collection in enumerate(collections):
        if name == collection["name"]:
            del collections[index]
            replace_database("collections", collections)
            print("Collection removed successfully.")
            time.sleep(.5)
            return
    print("Collection does not exist.")
    time.sleep(.5)

def edit_collection():
    collections = load_database("collections")
    if not collections:
        print("You dont have any collection.")
        time.sleep(.5)
        return
    old_name = name_input("Collection")
    if not old_name:
        return
    for index, collection in enumerate(collections):
        if old_name == collection["name"]:
            while True:
                new_name = name_input("new collection", all_keyword=True)
                if not new_name:
                    return
                elif new_name == old_name:
                    print("Please enter a new name.")
                elif any(col["name"] == new_name for col in collections):
                    print("This name is already in use by another collection.")
                else:
                    collections[index]["name"] = new_name
                    collections[index]["date updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    replace_database("collections", collections)
                    print("Collection name updated successfully.")
                    time.sleep(.5)
                    return
    print("Collection does not exist.")
    time.sleep(.5)

def print_collections():
    collections = load_database("collections")
    if not collections:
        print("You dont have any collection.")
        time.sleep(.5)
        return
    movies = load_database("movies")
    for index, collection in enumerate(collections):
        print(f"{index + 1}. {collection['name']}")
        temp_collection = collection.copy()
        del temp_collection["name"]
        del temp_collection["items"]
        for key, value in temp_collection.items():
            print(f"   {key.capitalize()}: {value}")
        found_movies = [list(movie.keys())[0] for movie in movies if list(movie.keys())[0] in collection["items"]]
        print_movie_by_id(found_movies, "   ")

def add_to_collection():
    movies = load_database("movies")
    if not movies:
        print("You dont have any movies")
        time.sleep(.5)
        return
    collection_name = name_input("Collection", False)
    if not collection_name:
        return
    collections = load_database("collections")
    for index, collection in enumerate(collections):
        if collection_name == collection["name"]:
            while True:
                selected_movies = search_select_movie(movies)
                if not selected_movies:
                    return
                for selected_movie in selected_movies:
                    movie_id = selected_movie
                    if movie_id in collection["items"]:
                        print("Movie already added.")
                        continue
                    collections[index]["items"].append(movie_id)
                    collections[index]["date updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    replace_database("collections", collections)
                    print("Movie added to collection successfully.")
    print("Collection does not exist")
    time.sleep(.5)

def remove_from_collection():
    movies = load_database("movies")
    if not movies:
        print("You dont have any movies")
        time.sleep(.5)
        return
    collection_name = name_input("collection", False)
    if not collection_name:
        return
    collections = load_database("collections")
    for index, collection in enumerate(collections):
        if collection_name == collection["name"]:
            found_movie_id = collection["items"]
            print_movie_by_id(found_movie_id)
            if not found_movie_id:
                print("collection dose not have any movie")
                return
            selected_movies = ask_for_select(len(found_movie_id))
            if not selected_movies:
                return
            if selected_movies == 1.5:
                collections[index]["items"] = []
                collections[index]["date updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                replace_database("collections", collections)
                print("All the Movies removed from collection successfully.")
                time.sleep(.5)
                return
            for selected_movie in sorted(selected_movies, reverse=True):
                collections[index]["items"].pop(selected_movie - 1)
                collections[index]["date updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                replace_database("collections", collections)
                print("Movie removed from collection successfully.")
            time.sleep(.5)
            return
    print("Collection does not exist")
    time.sleep(.5)


# movie
def add_movie():
    while True:
        name = name_input(all_keyword=True)
        if not name:
            return
        movies = load_database("movies")
        movie = {
            str(uuid.uuid4()):
                {
                    "name": name,
                    "release year": release_year_input(),
                    "genre": multi_string_input("genre"),
                    "language": multi_string_input("language"),
                    "country": multi_string_input("country"),
                    "type": type_input(required=True),
                    "imdb": imdb_input(),
                    "summery": summary_input(),
                    "img url": None,
                    "rate": rate_input(),
                    "have seen": have_seen_input(required=True),
                    "date added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        }
        if check_movie_exist(movies, movie):
            print("Movie already exists")
        else:
            update_database("movies", movie)
            print("Movie added successfully.")
            time.sleep(.5)
            return

def remove_movie():
    movies = load_database("movies")
    if not movies:
        print("You dont have any movies")
        time.sleep(.5)
        return
    selected_movies_id = search_select_movie(movies)
    if selected_movies_id == 1.5:
        while True:
            check_answer = input("Are you sure you want to remove all movies? (Y/N): ").strip().upper()
            if check_answer == "Y":
                movies = []
                replace_database("movies", movies)
                print("Movies are removed successfully.")
                time.sleep(.5)
                return
            elif check_answer == "N":
                return
    collections = load_database("collections")
    if not selected_movies_id:
        return
    collection_change = False
    for movie_id in selected_movies_id:
        for col_index, col in enumerate(collections):
            if movie_id in col["items"]:
                collection_change = True
                collections[col_index]["items"].remove(movie_id)
        for index, movie in enumerate(movies):
            if movie_id == list(movie.items())[0][0]:
                movies.pop(index)
                print("Movie removed successfully.")
    replace_database("movies", movies)
    if collection_change:
        replace_database("collections", collections)
    time.sleep(.5)

def edit_movie():
    movies = load_database("movies")
    if not movies:
        print("You dont have any movies")
        time.sleep(.5)
        return
    while True:
        selected_movie_id = search_select_movie(movies, False)
        print(selected_movie_id)
        if not selected_movie_id:
            return
        selected_movie = None
        for movie in movies:
            if selected_movie_id == list(movie.keys())[0]:
                selected_movie = movie[selected_movie_id]
                break
        if not selected_movie:
            print("Selected movie not found.")
            return

        attribute_functions = {
            "name": lambda: name_input("new movie", all_keyword=True),
            "release year": release_year_input,
            "genre": lambda: multi_string_input("genre"),
            "language": lambda: multi_string_input("language"),
            "country": lambda: multi_string_input("country"),
            "type": type_input,
            "imdb": imdb_input,
            "summery": summary_input,
            "rate": rate_input,
            "have seen": have_seen_input
        }
        detail_len = print_movie_items(selected_movie_id)
        selected_index = ask_for_select(detail_len, required=False)
        if not selected_index:
            break
        if isinstance(selected_index, int):
            selected_index = [selected_index]
        for item_index in selected_index:
            while True:
                selected_item = list(selected_movie.keys())[item_index - 1]
                if selected_item not in attribute_functions:
                    print("Invalid attribute selected.")
                    break
                new_value = attribute_functions[selected_item]()
                if selected_item in ["name", "type", "have seen"] and new_value is None:
                    break
                if new_value == selected_movie[selected_item]:
                    break
                selected_movie[selected_item] = new_value
                replace_database("movies", movies)
                print("Selected items updated successfully.")
                break
        time.sleep(.5)
        return

def print_movies():
    movies = load_database("movies")
    if not movies:
        print("You dont have any movies")
        time.sleep(.5)
        return
    for index, each_movie in enumerate(movies):
        movie_id = list(each_movie.keys())[0]
        movie = each_movie[movie_id]
        print(f"{index + 1}:")
        for key, value in movie.items():
            print(f"   {key.capitalize()}: {"N/A" if value is None else value}")
    time.sleep(.5)


# operators
#01
def main_operator():
    while True:
        main_operator_input = input("select operator category to use (1-Movie 2-Collection 3-Search): ")
        if not main_operator_input:
            return
        if not main_operator_input.isdigit():
            print("Please enter a number")
            time.sleep(.5)
            continue
        main_operator_input = int(main_operator_input)
        match main_operator_input:
            case 1:
                movie_operator()
            case 2:
                collection_operator()
            case 3:
                search_database()
            case _:
                print("Please enter 1 or 2")
                time.sleep(.5)
                continue

def movie_operator():
    while True:
        print("1-Add Movie")
        print("2-Remove Movie")
        print("3-Edit Movie")
        print("4-Search Movie")
        print("5-Print Movie")
        movie_operator_input = input("what do you want to do?: ")
        if not movie_operator_input:
            return
        if not movie_operator_input.isdigit():
            print("Please enter a number")
            time.sleep(.5)
            continue
        movie_operator_input = int(movie_operator_input)
        match movie_operator_input:
            case 1:
                add_movie()
            case 2:
                remove_movie()
            case 3:
                edit_movie()
            case 4:
                search_database("movies")
            case 5:
                print_movies()
            case _:
                print("Please enter number between 1 and 5")
                time.sleep(.5)
                continue

def collection_operator():
    while True:
        print("1-add collection")
        print("2-remove collection")
        print("3-edit collection")
        print("4-search collection")
        print("5-add movie to collection")
        print("6-remove movie from collection")
        print("7-print collections")
        collection_operator_input = input("what do you want to do?: ")
        if not collection_operator_input:
            return
        if not collection_operator_input.isdigit():
            print("Please enter a number")
            time.sleep(.5)
            continue
        collection_operator_input = int(collection_operator_input)
        match collection_operator_input:
            case 1:
                add_collection()
            case 2:
                remove_collection()
            case 3:
                edit_collection()
            case 4:
                search_database("collections")
            case 5:
                add_to_collection()
            case 6:
                remove_from_collection()
            case 7:
                print_collections()
            case _:
                print("Please enter number between 1 and 7")
                time.sleep(.5)
                continue

#02
def help_command():
    print("Global Command:")
    print("\texit = Exit")
    print("\tf = Search")
    print("Movie Command:")
    print("\tam = Add Movie")
    print("\trm = Remove Movie")
    print("\tem = Edit Movie")
    print("\tfm = Search Movie")
    print("\tsm = Sort Movie")
    print("\tmp = Print Movie")
    print("Collection Command:")
    print("\tac = Add Collection")
    print("\trc = Remove Collection")
    print("\tec = Edit Collection")
    print("\tfc = Search Collection")
    print("\tsc = Sort Collection")
    print("\tcam = Add to Collection")
    print("\tcrm = Remove from Collection")
    print("\tpc = Print Collection")
    time.sleep(1)

def operator():
    while True:
        operator_input = input("Enter Command (?): ").strip().lower()
        if operator_input == "exit":
            return
        if not operator_input:
            continue
        match operator_input:
            case "?":
                help_command()
            case "f":
                search_database()
            case "am":
                add_movie()
            case "rm":
                remove_movie()
            case "em":
                edit_movie()
            case "fm":
                search_database("movies")
            case "sm":
                sort_database("movies")
            case "pm":
                print_movies()
            case "ac":
                add_collection()
            case "rc":
                remove_collection()
            case "ec":
                edit_collection()
            case "fc":
                search_database("collections")
            case "sc":
                sort_database("collections")
            case "cam":
                add_to_collection()
            case "crm":
                remove_from_collection()
            case "pc":
                print_collections()
            case _:
                print("Enter a valid command")
                time.sleep(.5)
                continue

operator()