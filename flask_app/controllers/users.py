from flask import render_template, session,redirect, request,flash, url_for, request
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import user,movie
# import os
import json




bcrypt = Bcrypt(app)

# pass = os.environ.get('FLASK_APP_API_KEY')
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('search_movie'))

    return render_template('index.html.j2')

@app.route('/reg/', methods = ['POST'])
def reg():
    if not user.User.validate_user(request.form):
        return redirect('/')
    data = {
        'user_name': request.form['user_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = user.User.save(data)
    session['user_id'] = id
    session['user_name'] = request.form['user_name']
    return redirect(url_for('search_movie'))

@app.route('/log/', methods = ['POST'])
def log():
    data = {
        "email": request.form['email']
    }
    
    tempUser = user.User.get_by_email(data)
    if not (user.User.check_existence(data)):
        flash("Invalid Email/Password","log")
        return redirect('/')
    if not tempUser:
        flash("Invalid Email/Password","log")
        return redirect("/")
    
    if not bcrypt.check_password_hash(tempUser.password,request.form['password']):
        flash("Invalid Email/Password","log")
        return redirect("/")
    session['user_id'] = tempUser.id
    session['user_name'] = tempUser.user_name
    return redirect(url_for('search_movie'))





@app.route('/search-movie/', methods=['GET', 'POST'])
def search_movie():
    if 'user_id' in session:
        result = {
        'id': session['user_id'],
        }
        ourimdb = user.User.user_has_movies(result)
        print(ourimdb)
        data = {
        'ourimdb': ourimdb,
        'id': session['user_id'],
        'name': session['user_name']
        
        } 
        return render_template('search-movie.html.j2',data=json.dumps(data))
    
    return render_template('search-movie.html.j2')



@app.route('/seen/<imdb_id>/', methods=['POST'])
def seen(imdb_id):
    if 'user_id' not in session:
        return redirect('/')
    checker = {
        'imdb_id': imdb_id
    }
    if (movie.Movie.validate_movie(checker)):
        data = {
        'movie_name': request.form['movie_name'],
        'imdb_id': request.form['imdb_id'],
        'img_src': request.form['img_src'],
        'year': request.form['year'],
        'description': request.form['description'],
        'imdb_rating': request.form['imDbRating']      
        }
        movie_id = movie.Movie.save(data)
        movie_user = {
        'users_id': session['user_id'],
        'movies_id': movie_id,
        'type': 'seen',
            }
             
        movie.Movie.insert_to_seen(movie_user)
        return redirect(url_for('search_movie'))
    
    movie_id = movie.Movie.search_by_imdb_id(imdb_id)
    movie_user = {
        'user_id': session['user_id'],
        'movie_id': movie_id.id,
        'type': 'seen',
    }
    movie.Movie.replace_in_seen(movie_user)
    return redirect(url_for('search_movie'))

@app.route('/future/')
def future(): 
    
    return redirect(url_for('search_movie'))

@app.route('/seen/')
def seen_page():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id':session['user_id'],
        'type': 'seen',
    }
    seen = user.User.get_seen(data)

    return render_template('seen.html.j2', seen=seen)

@app.route('/unseen/<movie_id>')
def unseen(movie_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'movie_id': movie_id,
        'user_id': session['user_id'],
        'type': 'NULL'
    }
    movie.Movie.unsee(data)
    return redirect(url_for('seen_page'))



@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')



# @app.route('searching', methods =['POST'])
# def req():
#     print(request.form['query'])
#     r = requests.get(f"https://imdb-api.com/API/AdvancedSearch/{os.environ.get('FLASK_API_KEY')}?user_rating={user_min},{user_max}&genres={genre},film_noir&count=100")


# @app.route("/search_res_check")
# def results_list_checked():
#     seen = User.query.seen(User.name).all()
#     movies = fetched_datak
#     results = for movies not in seen
#      Movie.query.order_by(User.name).all()
#     return jsonify([u.to_json() for u in results])

# @app.route('/query/')
# def query():

    # args = request.args
    # 
    # for k, v in args.items():
    #     print(f"{k}: {v}")
    # 
    # if "foo" in args:
    #     foo = args.get("foo")
    #     print(foo)
# 
    # if request.args:
    #     args = request.args
    #     if "title" in args:
    #         title = request.args.get("title")
    #         print(title)
# 
    # if request.args:
    #     args =request.args
    #     if session['user'] in session:
# 
    # if request.args:
    #     args = request.args
    #     serialized = ", ".join(f"{k}: {v}" for k, v in args.items())
    #     return f"(Query) {serialized}", 200
    # else:
# 
    # print(request.query_string)
    # return "No query received", 200