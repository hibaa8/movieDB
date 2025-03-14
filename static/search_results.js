function displayPopularMovies(popular_movies) {
    let container = $("#pop-movie-container");
    container.empty(); // Clear existing content

    let row;
    $.each(popular_movies, function(i, movie) {
        if (i % 3 === 0) { // Create a new row every 3 movies
            row = $('<div class="row"></div>');
            container.append(row);
        }

        let movieDiv = `
            <div class="col-md-4">
                <div class="movie-card">
                    <a href="/view/${movie.id}">
                        <img src="${movie.image}" alt="${movie.title} poster" class="movie-image">
                    </a>
                    <h3>${movie.title}</h3>
                    <p><strong>Release Year:</strong> ${movie.release_year}</p>
                    <p><strong>IMDb Rating:</strong> ${movie.ratings.imdb}</p>
                </div>
            </div>
        `;

        row.append(movieDiv);
    });
}

function save_movie(newMovie) {
    console.log('new movie');
    console.log(newMovie)
    $.ajax({
        type: "POST",
        url: "/add",               
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newMovie),
        success: function (result) {
            $("#movie-success-message").html(`
                <h5>Movie page created. View it <a href="/view/${result.movie.id}">here</a></h5>
            `).show();
            $("#add-movie-form")[0].reset();
            $("#movie-title").focus();
        },
        error: function (request, status, error) {
            console.error("Error adding movie:", error);
            alert("Failed to add movie. Please try again.");
        }
    });
}

function update_movie(updatedMovie,movieId){
    $.ajax({
        type: "POST",
        url: `/edit/${movieId}`,
        data: JSON.stringify(updatedMovie),
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            window.location.href = `/view/${movieId}`;
        },
        error: function (request, status, error) {
            console.error("Error updating movie:", error);
            alert("Failed to update movie. Please try again.");
        }
    });
}


$(document).ready(function(){
    if (typeof popular_movies !== "undefined" && $("#pop-movie-container").is(":empty")) {  
        displayPopularMovies(popular_movies);
    }    
    $( ".d-flex" ).on( "submit", function( event ) {
        let field = $( "#search-input-field" )
        let query = field.val().trim();
        if ( query.length == 0) {
            event.preventDefault();
            field.val("")
            field.focus()
        }
    }) 
    $('#submit-movie-btn').click(function (event) {
        event.preventDefault();
        let title = $('#movie-title').val().trim();
        let image = $('#movie-image').val().trim();
        let release_year = $('#release-year').val().trim();
        let summary = $('#movie-summary').val().trim();
        let director = $('#directors').val().trim();
        let actors = $('#actors').val().trim();
        let budget = $('#budget').val().trim();
        let imdb = $('#imdb').val().trim();
        let rotten_tomatoes = $('#rotten_tomatoes').val().trim();
        let common_sense = $('#common_sense').val().trim();
        let google_ratings = $('#google_ratings').val().trim();
        let genres = $('#genres').val().trim();
        let similar_movie_ids = $('#similar-movies').val().trim();
    
        // Convert comma-separated inputs to lists
        let directorList = director ? director.split(',').map(item => item.trim()) : [];
        let actorsList = actors ? actors.split(',').map(item => item.trim()) : [];
        let genresList = genres ? genres.split(',').map(item => item.trim()) : [];
        let similarMovieList = similar_movie_ids ? similar_movie_ids.split(',').map(item => parseInt(item.trim())) : [];
    
        // Validate required fields
        if (!title || !release_year || !genres) {
            alert("You must complete all fields");
            return;
        }
    
        let newMovie = {
            "title": title,
            "image": image,
            "release_year": release_year,
            "summary": summary,
            "director": directorList,
            "actors": actorsList,
            "budget": budget ? parseInt(budget) : 0,
            "ratings": {
                "imdb": imdb,
                "rotten_tomatoes": rotten_tomatoes,
                "common_sense": common_sense,
                "google_ratings": google_ratings
            },
            "genres": genresList,
            "similar_movie_ids": similarMovieList
        };
        console.log(newMovie)
        save_movie(newMovie);
    });    

    
    $('#submit-edit').click(function (event) {
        event.preventDefault();
        let movieId = $("#movie-id").val();
        let updatedMovie = {
            "title": $("#title").val().trim(),
            "release_year": $("#release_year").val().trim(),
            "summary": $("#summary").val().trim(),
            "director": $("#director").val().trim().split(",").map(d => d.trim()),
            "actors": $("#actors").val().trim().split(",").map(a => a.trim()),
            "budget": parseInt($("#budget").val().trim()) || 0,
            "genres": $("#genres").val().trim().split(",").map(g => g.trim()),
            "ratings": {
                "imdb": $("#imdb").val().trim(),
                "rotten_tomatoes": $("#rotten_tomatoes").val().trim() + "%",  // Ensure % symbol
                "common_sense": $("#common_sense").val().trim() + "/5",  // Ensure "/5" format
                "google_ratings": $("#google_ratings").val().trim() + "%"  // Ensure % symbol
            }
        };

        console.log(updatedMovie)
        update_movie(updatedMovie, movieId) 
    });

    $("#discard-edit").click(function () {
        if (confirm("Are you sure you want to discard changes?")) {
            let movieId = $("#movie-id").val();
            window.location.href = `/view/${movieId}`;
        }
    });

})