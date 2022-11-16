var search_form = document.getElementById("search_form");
var our_result = document.getElementById("our_result");
var min_rating = document.getElementById("min_rating");
var max_rating = document.getElementById("max_rating");
var cboxes = document.getElementsByName("genres");
var elmntToView = document.getElementById("results");
var logged = false;
var ourImdbArray = [];

search_form.onsubmit = function (e) {
  e.preventDefault();
  var checkedValue = [];
  var len = cboxes.length;
  for (var i = 0; i < len; i++) {
    if (cboxes[i].checked) {
      checkedValue.push(cboxes[i].value);
    }
  }
  let genres = checkedValue.join(", ");
  var entry = {
    min_rating: min_rating.value,
    max_rating: max_rating.value,
    genre: genres,
  };
  var our_movie = {};
  getMovie();
  async function getMovie() {
    our_result.innerHTML = `
    <div class="container">
    <div class="row-10">
    <div class="col-12 text-center text-white">
    <h1> Loading movie for you!<h1>
    <h2> Please wait a second</h2>
    <img src="https://th.bing.com/th/id/R.18288dfd323213083500dc4b8f9820e2?rik=iHxnlNP3XvLo%2bg&pid=ImgRaw&r=0" alt="loading" width="30%" style="border-radius: 25%">
    </div>
    </div>
    </div>
    `;

    var response = await fetch(
      `https://imdb-api.com/API/AdvancedSearch/k_1t185h9p?title_type=tv_movie&user_rating=${entry.min_rating}.0,${entry.max_rating}.0&genres=${entry.genre}&count=100`
    );

    var data = await response.json();

    const getRandomMovie = function () {
      let movie, cur_index;
      let our_data = data.results;
      let lengthofres = data.results.length;

      const search = function () {
        cur_index = Math.floor(Math.random() * lengthofres);
        movie = our_data[cur_index];
      };
      search();
      while (lengthofres > 0 && ourImdbArray.includes(movie.id)) {
        our_data.splice(cur_index, 1);
        lengthofres - 1;
        search();
      }
      if (lengthofres == 0) return false;
      return movie;
    };

    our_movie = getRandomMovie();

    if (!our_movie) {
      our_result.innerHTML = `
    <div class="container">
    <div class="row-10">
    <div class="col-12 text-center text-white">
    <h1> Sorry we couldn't find anything by this request please apply different filters<h1>
    </div>
    </div>
    </div>
    `;
    }

    let buttons = `
    <div class="text-center" style=" margin-top: 1%;">
  <button type="submit" class =" btn btn-success btn-sm mr-5">Mark as seen</button>
  </div>`;
    // <button type="submit" formaction="/future/" class =" btn btn-info btn-sm ml-5">Save for future</button>

    our_result.innerHTML = `
    <form  action="/seen/${our_movie.id}/" method="post">
    <div class="container">
      <div class="row-8">
        <div id="results" class="col-8 text-center text-white mx-auto" >
        <div class="card bg-transparent text-white text-center mx-auto">
        <div class="col-6" style="margin: 0 auto">
          <img
            src="${our_movie.image}"
            class="card-img-top col-6" width="100%"
            alt="${our_movie.title}"
            />
        </div>
          
          <div class="card-body" autofocus>
  
          <h3 class="card-title">${
            our_movie.title
          } <br> Year published: ${our_movie.description.slice(
      1,
      5
    )} <br> IMDB Rating: ${our_movie.imDbRating} ★ / 10.0 ★</h3>
            
            <p id = "plot" class="card-text">${our_movie.plot}</p>
            
            <input type="hidden" name="imdb_id" value="${our_movie.id}">
            <input type="hidden" name="movie_name" value="${our_movie.title}">
            <input type="hidden" name="img_src" value="${our_movie.image}">
            <input type="hidden" name="year" value="${our_movie.description.slice(
              1,
              5
            )}">
            <input type="hidden" name="imDbRating" value="${
              our_movie.imDbRating
            }">
            <input type="hidden" name="description" value="${our_movie.plot}">
            </div>
            </div>
            </div>
            </div>
            </div>
            ${logged ? buttons : ""}
            </form>
            `;
  }
};
const listOfImdb = function (arr) {
  for (const every of arr) {
    ourImdbArray.push(every.imdb_id);
  }
};
const ifLoged = function (value) {
  logged = value;
};
