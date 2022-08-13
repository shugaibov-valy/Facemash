import random
import uuid
from db import Base, session
from flask_cors import cross_origin
from flask import Flask, Blueprint, render_template, redirect, url_for, request, make_response, jsonify
from utils import calc_elo
import flask
from components.users.models import User
from components.votes.models import Vote


app = Flask(__name__)

# This function close the session
@app.teardown_appcontext
def shutdown_session(exception=None):
    from db import session
    session.remove()

@app.route("/")
def index():
    users = session.query(User).all()
    u1 = random.choice(users)
    u2 = random.choice(users)
    users = User.get_top_users()       
    return render_template("index.html", left=u1, right=u2, top_users=users)

@app.route("/update_table", methods=['GET', 'POST'])
def update_table():
    if flask.request.method == "POST":
        users = User.get_top_users()
        return jsonify('', render_template("table.html", top_users=users))

@app.route("/search_user/vk_id=<string:vk_id>", methods=['GET', 'POST'])
def search_user(vk_id):
    if flask.request.method == "POST":
        user = User.get_user_by_vkid(vk_id)
        return jsonify('', render_template("table_for_search_user.html", 
user=user))


@app.route("/update_raiting/vk_id=<int:vk_id>")
def update_raiting(vk_id):
    User.update_rating(vk_id, 1)
    return jsonify(1)


@app.route("/random_user")
def random_user():
    users = User.query.order_by(User.rating).all()
    if len(users):
        votes = Vote.query.filter_by(uuid=request.cookies.get('uuid')).all()
        goods = set(range(1, len(users))) - {vote.win_id for vote in votes}
        if len(goods) < 3:
            pass 
        user = random.choice(list(goods)) 
        return jsonify([User.query.get(user).vk_id, User.query.get(user).photo])
 

@app.post("/vote")
@cross_origin(supports_credentials=True)
def vote():
    r = request.get_json()
    print(r)
    if 'win_id' in list(r.keys()) and 'lose_id' in list(r.keys()) and 'cookie' in list(r.keys()):
        win_id, lose_id = r['win_id'], r['lose_id']
        q = db.session.query(User, Vote.win_id).outerjoin(Vote, User.vk_id == Vote.win_id).filter(
            Vote.win_id is None).all()
        print(q)
        votes = Vote.query.filter_by(
            uuid=r['cookie']).all()  # Выгражает все данные о опросе в память <------------- !!!!!!
        print(votes)
    #     dump = {vote.win_id for vote in votes} | {vote.lose_id for vote in votes}
    #     win_id, lose_id = request.json['win_id'], request.json['lose_id']
    #     if (int(win_id) in dump) or (int(lose_id) in dump):
    #         return redirect(url_for("index"))
    #     win, lose = User.query.get(win_id), User.query.get(lose_id)
    #     if (not win) or (not lose):
    #         return redirect(url_for("index"))
    #     win_elo, win_times = win.rating, win.times
    #     lose_elo, lose_times = lose.rating, lose.times
    #     win_elo = calc_elo(1, float(win_elo), float(lose_elo), int(win_times))
    #     lose_elo = calc_elo(0, float(lose_elo), float(win_elo), int(lose_times))
    #     win.elo, win.times = win_elo, win_times + 1
    #     lose.elo, lose.times = lose_elo, lose_times + 1
    #     Vote(request, win_id, lose_id).save()
    #     win.save(), lose.save()
    #     dump.add(win_id), dump.add(lose_id)
    #     choice = random.choice(list(set(range(1, User.query.count())) - {dump}))
        return jsonify({"choice": "choice"})
    print(request.json)
    return jsonify({"error": "fuck"})




# @app.route("/livesearch", methods=["POST", "GET"])
# def livesearch():
#     searchbox = request.form.get("text")
#     # cursor = mysql.connection.cursor()
#     query = "select world_eng from words where word_eng LIKE '{}%' order by word_eng".format(searchbox)
#     cursor.execute(query)
#     result = cursor.fetchall/()
#     return jsonify(result)




@app.route("/posts")
def posts():
    users = User.query.order_by(User.photo).all()
    return render_template("posts.html", users=users)






