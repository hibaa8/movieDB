// function displayPopularMovies(popular_movies) {
//     let container = $("#pop-movie-container");
//     container.empty(); // Clear existing content

//     let row;
//     $.each(popular_movies, function(i, movie) {
//         if (i % 3 === 0) { // Create a new row every 3 movies
//             row = $('<div class="row"></div>');
//             container.append(row);
//         }

//         let movieDiv = `
//         <div class="col-md-4">
//             <div class="movie-container">
//                 <a href="/view/${ movie.id }">
//                     <img src="${ movie.image }" alt="${ movie.title } poster" class="movie-image">
//                 </a>
//                 <div class="movie-info">
//                     <h4 class="movie-title">${ movie.title }</h4>
//                     <p class="movie-details"><strong>Release Year:</strong> ${ movie.release_year }</p>
//                     <p class="movie-details"><strong>IMDb Rating:</strong> ${ movie.ratings.imdb }</p>
//                 </div>
//             </div>
//         </div>
//         `;

//         row.append(movieDiv);
//     });
// }

function displayPopularMovies(popular_movies) {
    let container = $("#pop-movie-container");
    container.empty(); // Clear existing content

    let row = $('<div class="row g-3"></div>'); // Add spacing between columns
    container.append(row);

    $.each(popular_movies, function(i, movie) {
        let movieDiv = `
        <div class="col-md-4 d-flex align-items-stretch">
            <div class="movie-container">
                <a href="/view/${ movie.id }">
                    <img src="${ movie.image }" alt="${ movie.title } poster" class="movie-image">
                </a>
                <div class="movie-info">
                    <p class="movie-title-card">${ movie.title }</p>
                    <p class="movie-details"><strong>Release Year:</strong> ${ movie.release_year }</p>
                    <p class="movie-details"><strong>IMDb Rating:</strong> ${ movie.ratings.imdb }</p>
                </div>
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

function showError(inputId, message) {
    $(inputId).after(`<small class="error-message text-danger">${message}</small>`);
}

function isValidUrl(string) {
    let urlPattern = new RegExp("^(https?:\\/\\/)?"+ // Protocol
        "((([a-zA-Z\\d]([a-zA-Z\\d-]*[a-zA-Z\\d])*)\\.)+[a-zA-Z]{2,}|" + // Domain name
        "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR IP
        "(\\:\\d+)?(\\/[-a-zA-Z\\d%@_.~+&:]*)*" + // Port and path
        "(\\?[;&a-zA-Z\\d%@_.,~+&:=-]*)?" + // Query string
        "(\\#[-a-zA-Z\\d_]*)?$", "i"); // Fragment locator
    return !!urlPattern.test(string);
}

function isValidRating(value) {
    return /^\d+(\.\d+)?$/.test(value) && parseFloat(value) >= 0 && parseFloat(value) <= 10;
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
        $(".is-invalid").removeClass("is-invalid"); // Remove red borders
        $(".invalid-feedback").remove(); // Remove existing error messages
    
        let isValid = true;
    
        // Get input values
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
    
        function validateField(selector, condition, errorMsg) {
            if (!condition) {
                let inputField = $(selector);
    
                if (!inputField.next(".invalid-feedback").length) {
                    inputField.addClass("is-invalid").after(`<div class="invalid-feedback">${errorMsg}</div>`);
                }
    
                isValid = false;
            } else {
                $(selector).removeClass("is-invalid").next(".invalid-feedback").remove(); 
            }
        }
    
        validateField("#movie-title", title.length > 0, "Movie title is required.");
        validateField("#release-year", /^\d{4}$/.test(release_year), "Enter a valid 4-digit year.");
        validateField("#movie-image", isValidUrl(image), "Enter a valid image URL.");
        validateField("#movie-summary", summary.length > 0, "Summary cannot be empty.");
        validateField("#directors", /^([a-zA-Z\s]+,?\s*)+$/.test(director), "Enter valid names separated by commas.");
        validateField("#actors", /^([a-zA-Z\s]+,?\s*)+$/.test(actors), "Enter valid names separated by commas.");
        validateField("#budget", /^\d+$/.test(budget) && parseInt(budget) >= 0, "Enter a non-negative budget.");
        validateField("#imdb", isValidRating(imdb), "Enter a rating between 0 and 10.");
        validateField("#rotten_tomatoes", isValidRating(rotten_tomatoes), "Enter a rating between 0 and 10.");
        validateField("#common_sense", isValidRating(common_sense), "Enter a rating between 0 and 10.");
        validateField("#google_ratings", isValidRating(google_ratings), "Enter a rating between 0 and 10.");
        validateField("#genres", /^([a-zA-Z\s]+,?\s*)+$/.test(genres), "Enter valid genres separated by commas.");
        validateField("#similar-movies", /^(\d+,?\s*)+$/.test(similar_movie_ids), "Enter valid movie IDs, separated by commas.");
        
    
        if (!isValid) return;

        let directorList = director ? director.split(',').map(item => item.trim()) : [];
        let actorsList = actors ? actors.split(',').map(item => item.trim()) : [];
        let genresList = genres ? genres.split(',').map(item => item.trim()) : [];
        let similarMovieList = similar_movie_ids ? similar_movie_ids.split(',').map(item => parseInt(item.trim())) : [];

            
        let newMovie = {
            "title": title,
            "image": image,
            "release_year": release_year,
            "summary": summary,
            "director": director,
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

    
    $('#submit-edit-btn').click(function (event) {
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
                "rotten_tomatoes": $("#rotten_tomatoes").val().trim() + "%", 
                "common_sense": $("#common_sense").val().trim() + "/5",  
                "google_ratings": $("#google_ratings").val().trim() + "%"  
            }
        };

        console.log(updatedMovie)
        update_movie(updatedMovie, movieId) 
    });

    $("#discard-edit-btn").click(function () {
        if (confirm("Are you sure you want to discard changes?")) {
            let movieId = $("#movie-id").val();
            window.location.href = `/view/${movieId}`;
        }
    });

})