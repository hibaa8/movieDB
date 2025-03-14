from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import random 
import re

app = Flask(__name__)

movie_id = 12
data = {
    1: {
        "id": "1",
        "title": "Dunki",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4f/Dunki_poster.jpg/220px-Dunki_poster.jpg",
        "release_year": "2023",
        "summary": "A group of friends set out on a perilous journey to emigrate to the United Kingdom via a clandestine route called 'donkey flight', risking their lives in the process.",
        "director": ["Rajkumar Hirani"],
        "actors": ["Shah Rukh Khan", "Taapsee Pannu", "Boman Irani", "Vikram Kochhar", "Anil Grover", "Vicky Kaushal"],
        "budget": 13700000,
        "ratings": {
            "imdb": "6.5", 
            "rotten_tomatoes": "46%", 
            "common_sense": "1/5",
            "google_ratings": "83%"
        },
        "genres": ["comedy", "romance", "adventure", "drama"],
        "similar_movie_ids": [4, 8, 11]
    },
    2: {
        "id": "2",
        "title": "Pathaan",
        "image": "https://upload.wikimedia.org/wikipedia/en/c/c3/Pathaan_film_poster.jpg",
        "release_year": "2023",
        "summary": "An exiled secret agent must protect India against a powerful terrorist organization with ties to his past.",
        "director": ["Siddharth Anand"],
        "actors": ["Shah Rukh Khan", "Deepika Padukone", "John Abraham", "Dimple Kapadia"],
        "budget": 31000000,
        "ratings": {
            "imdb": "7.0",
            "rotten_tomatoes": "80%",
            "common_sense": "3/5",
            "google_ratings": "88%"
        },
        "genres": ["action", "thriller", "spy"],
        "similar_movie_ids": [5, 6, 10]
    },
    3: {
        "id": "3",
        "title": "Kabhi Khushi Kabhie Gham",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Kabhi_Khushi_Kabhie_Gham..._poster.jpg/220px-Kabhi_Khushi_Kabhie_Gham..._poster.jpg",
        "release_year": "2001",
        "summary": "A wealthy businessman's adopted son is disowned when he marries a woman from a lower social class.",
        "director": ["Karan Johar"],
        "actors": ["Shah Rukh Khan", "Kajol", "Amitabh Bachchan", "Jaya Bachchan", "Hrithik Roshan", "Kareena Kapoor"],
        "budget": 12000000,
        "ratings": {
            "imdb": "7.4",
            "rotten_tomatoes": "92%",
            "common_sense": "4/5",
            "google_ratings": "94%"
        },
        "genres": ["family", "drama", "romance"],
        "similar_movie_ids": [7, 9, 11]
    },
    4: {
        "id": "4",
        "title": "3 Idiots",
        "image": "https://m.media-amazon.com/images/M/MV5BNzc4ZWQ3NmYtODE0Ny00YTQ4LTlkZWItNTBkMGQ0MmUwMmJlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "release_year": "2009",
        "summary": "Two friends set out on a journey to find their long-lost college buddy, recalling their college days and the impact of their mentor.",
        "director": ["Rajkumar Hirani"],
        "actors": ["Aamir Khan", "R. Madhavan", "Sharman Joshi", "Kareena Kapoor"],
        "budget": 10000000,
        "ratings": {
            "imdb": "8.4",
            "rotten_tomatoes": "100%",
            "common_sense": "5/5",
            "google_ratings": "96%"
        },
        "genres": ["comedy", "drama"],
        "similar_movie_ids": [1, 8, 10]
    },
    5: {
        "id": "5",
        "title": "Jawan",
        "image": "https://upload.wikimedia.org/wikipedia/en/3/39/Jawan_film_poster.jpg",
        "release_year": "2023",
        "summary": "A vigilante sets out on a mission to fight against corruption and injustice with the help of a mysterious past.",
        "director": ["Atlee"],
        "actors": ["Shah Rukh Khan", "Nayanthara", "Vijay Sethupathi", "Deepika Padukone"],
        "budget": 33000000,
        "ratings": {
            "imdb": "7.2",
            "rotten_tomatoes": "85%",
            "common_sense": "4/5",
            "google_ratings": "89%"
        },
        "genres": ["action", "thriller"],
        "similar_movie_ids": [2, 6, 10]
    },
    6: {
        "id": "6",
        "title": "Gangs of Wasseypur",
        "image": "https://m.media-amazon.com/images/M/MV5BMTc5NjY4MjUwNF5BMl5BanBnXkFtZTgwODM3NzM5MzE@._V1_.jpg",
        "release_year": "2012",
        "summary": "A crime saga spanning generations of rivalry and revenge in the coal mafia of Dhanbad.",
        "director": ["Anurag Kashyap"],
        "actors": ["Manoj Bajpayee", "Nawazuddin Siddiqui", "Richa Chadha"],
        "budget": 2700000,
        "ratings": {
            "imdb": "8.2",
            "rotten_tomatoes": "95%",
            "common_sense": "4/5",
            "google_ratings": "91%"
        },
        "genres": ["crime", "drama", "thriller"],
        "similar_movie_ids": [5, 10, 11]
    },
    7: {
        "id": "7",
        "title": "Dilwale Dulhania Le Jayenge",
        "image": "https://upload.wikimedia.org/wikipedia/en/8/80/Dilwale_Dulhania_Le_Jayenge_poster.jpg",
        "release_year": "1995",
        "summary": "A young man falls in love with a woman engaged to someone else and sets out to win over her conservative family.",
        "director": ["Aditya Chopra"],
        "actors": ["Shah Rukh Khan", "Kajol", "Amrish Puri"],
        "budget": 1000000,
        "ratings": {
            "imdb": "8.0",
            "rotten_tomatoes": "96%",
            "common_sense": "5/5",
            "google_ratings": "98%"
        },
        "genres": ["romance", "drama"],
        "similar_movie_ids": [3, 9, 11]
    },
    8: {
        "id": "8",
        "title": "Zindagi Na Milegi Dobara",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/1/17/Zindagi_Na_Milegi_Dobara.jpg/220px-Zindagi_Na_Milegi_Dobara.jpg",
        "release_year": "2011",
        "summary": "Three childhood friends reunite for a road trip across Spain, rediscovering love, life, and friendships along the way.",
        "director": ["Zoya Akhtar"],
        "actors": ["Hrithik Roshan", "Farhan Akhtar", "Abhay Deol", "Katrina Kaif", "Kalki Koechlin"],
        "budget": 8000000,
        "ratings": {
            "imdb": "8.2",
            "rotten_tomatoes": "92%",
            "common_sense": "4/5",
            "google_ratings": "94%"
        },
        "genres": ["adventure", "drama", "comedy"],
        "similar_movie_ids": [3, 5, 9]
    },
    9: {
        "id": "9",
        "title": "My Name is Khan",
        "image": "https://upload.wikimedia.org/wikipedia/en/5/5d/My_Name_Is_Khan_film_poster.jpg",
        "release_year": "2010",
        "summary": "An autistic man embarks on a journey across the United States to meet the President and convey a simple message: 'My name is Khan, and I am not a terrorist.'",
        "director": ["Karan Johar"],
        "actors": ["Shah Rukh Khan", "Kajol", "Jimmy Shergill", "Zarina Wahab", "Sonya Jehan"],
        "budget": 22000000,
        "ratings": {
            "imdb": "8.0",
            "rotten_tomatoes": "85%",
            "common_sense": "4/5",
            "google_ratings": "95%"
        },
        "genres": ["drama", "romance"],
        "similar_movie_ids": [3, 7, 9]
    },
    10: {
        "id": "10",
        "title": "Andhadhun",
        "image": "https://upload.wikimedia.org/wikipedia/en/4/47/Andhadhun_poster.jpg",
        "release_year": "2018",
        "summary": "A blind pianist gets caught in a web of crime and deception after unintentionally witnessing a murder.",
        "director": ["Sriram Raghavan"],
        "actors": ["Ayushmann Khurrana", "Tabu", "Radhika Apte"],
        "budget": 4500000,
        "ratings": {
            "imdb": "8.3",
            "rotten_tomatoes": "98%",
            "common_sense": "4/5",
            "google_ratings": "95%"
        },
        "genres": ["thriller", "mystery", "crime"],
        "similar_movie_ids": [4, 6, 9]
    },
    11: {
        "id": "11",
        "title": "Jab Tak Hai Jaan",
        "image": "https://upload.wikimedia.org/wikipedia/en/f/f9/Jab_Tak_Hai_Jaan_Poster.jpg",
        "release_year": "2012",
        "summary": "A bomb disposal expert, Samar, falls in love with Meera, but circumstances separate them. Years later, fate brings them back together in an unexpected way.",
        "director": ["Yash Chopra"],
        "actors": ["Shah Rukh Khan", "Katrina Kaif", "Anushka Sharma"],
        "budget": 12000000,
        "ratings": {
            "imdb": "6.7",
            "rotten_tomatoes": "90%",
            "common_sense": "3/5",
            "google_ratings": "91%"
        },
        "genres": ["romance", "drama"],
        "similar_movie_ids": [3, 7, 9]
    }
}

popular_movies = random.sample(list(data.values()), 3)

def get_rating_color(rating):
    rating = float(rating)//10 if rating else 0.0
    print(rating)
    if rating >= 5:
        return "bg-success"  # Dark green
    else:
        return "bg-warning"  # Yellow


app.jinja_env.globals.update(get_rating_color=get_rating_color)

# code by Hiba Altaf
@app.route('/')
def hello_world():
   return render_template('index.html', popular_movies=popular_movies)   

@app.route('/view/<int:item_id>')
def view_movie_page(item_id):
    movie = data.get(item_id)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_template.html', movie=movie, data=data)

@app.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get("query", "").strip().lower()
    query_words = query.split()  

    matching_movies = []

    for _, movie_info in data.items():
        matched_fields = []  
        highlighted_info = {} 

        def highlight_text(text, words):
            for word in words:
                text = re.sub(f"({re.escape(word)})", r"<span class='highlight'>\1</span>", text, flags=re.IGNORECASE)
            return text

        if any(word in movie_info["title"].lower() for word in query_words):
            matched_fields.append("Title")
            highlighted_info["title"] = highlight_text(movie_info["title"], query_words)
        else:
            highlighted_info["title"] = movie_info["title"]

        if any(word in director.lower() for director in movie_info.get("director", []) for word in query_words):
            matched_fields.append("Director")
            highlighted_info["director"] = [highlight_text(d, query_words) for d in movie_info["director"]]
        else:
            highlighted_info["director"] = movie_info["director"]

        if any(word in actor.lower() for actor in movie_info.get("actors", []) for word in query_words):
            matched_fields.append("Actors")
            highlighted_info["actors"] = [highlight_text(a, query_words) for a in movie_info["actors"]]
        else:
            highlighted_info["actors"] = movie_info["actors"]

        if any(word in genre.lower() for genre in movie_info.get("genres", []) for word in query_words):
            matched_fields.append("Genres")
            highlighted_info["genres"] = [highlight_text(g, query_words) for g in movie_info["genres"]]
        else:
            highlighted_info["genres"] = movie_info["genres"]

        if matched_fields:
            movie_info["highlighted"] = highlighted_info
            movie_info["matched_fields"] = matched_fields
            matching_movies.append(movie_info)

    result_count = len(matching_movies)

    return render_template('search_results.html', results=matching_movies, query=query, result_count=result_count, query_words=query_words)


@app.route('/add_movie')
def add_movie():
    return render_template("add_movie.html", new_movie_id="")
        

@app.route('/add', methods=['POST'])
def add():            
    global data  # Movie storage dictionary
    global movie_id
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400  # Bad request if JSON is missing
    # print(f'json data: {json_data}')

    movie_id += 1
    new_movie = {
        "id": movie_id,
        "title": json_data.get("title", ""),
        "image": json_data.get("image", ""),
        "release_year": json_data.get("release_year", ""),
        "summary": json_data.get("summary", ""),
        "director": json_data.get("director", []),
        "actors": json_data.get("actors", []),
        "budget": json_data.get("budget", 0),
        "ratings": json_data.get("ratings", {
            "imdb": "",
            "rotten_tomatoes": "",
            "common_sense": "",
            "google_ratings": ""
        }),
        "genres": json_data.get("genres", []),
        "similar_movie_ids": json_data.get("similar_movie_ids", [])
    }

    print(f'new movie')
    print(new_movie)

    data[movie_id] = new_movie  # Add movie to dictionary
    return jsonify({"message": "Movie added successfully", "movie": new_movie})

@app.route('/edit/<int:movie_id>')
def edit_movie(movie_id):
    movie = data.get(movie_id)
    if not movie:
        return "Movie not found", 404
    return render_template("edit_movie.html", movie=movie)

@app.route('/edit/<int:movie_id>', methods=['POST'])
def save_edit_movie(movie_id):
    if movie_id not in data:
        return jsonify({"error": "Movie not found"}), 404

    json_data = request.get_json(force=True, silent=True)
    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Update movie data
    data[movie_id].update({
        "title": json_data.get("title", data[movie_id]["title"]),
        "release_year": json_data.get("release_year", data[movie_id]["release_year"]),
        "summary": json_data.get("summary", data[movie_id]["summary"]),
        "director": json_data.get("director", data[movie_id]["director"]),
        "actors": json_data.get("actors", data[movie_id]["actors"]),
        "budget": int(json_data.get("budget", data[movie_id]["budget"])),
        "genres": json_data.get("genres", data[movie_id]["genres"]),
        "ratings": {
            "imdb": json_data["ratings"].get("imdb", data[movie_id]["ratings"]["imdb"]),
            "rotten_tomatoes": json_data["ratings"].get("rotten_tomatoes", data[movie_id]["ratings"]["rotten_tomatoes"]),
            "common_sense": json_data["ratings"].get("common_sense", data[movie_id]["ratings"]["common_sense"]),
            "google_ratings": json_data["ratings"].get("google_ratings", data[movie_id]["ratings"]["google_ratings"])
        }
    })

    return jsonify({"message": "Movie updated successfully", "movie": data[movie_id]}), 200


if __name__ == '__main__':
   app.run(debug = True, port=5001)




