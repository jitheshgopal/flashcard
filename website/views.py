from typing import Collection
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required,  current_user
from . import db
from .models import Collection, Card, User
import json

views = Blueprint('views',__name__)
@views.route('/' , methods = ['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        collection_name = request.form.get('name')
        if len(collection_name) < 1:
            flash('Name is too ahort',category='error')
        else:
            new_collection  = Collection(name=collection_name, user_id = current_user.id)
            db.session.add(new_collection)
            db.session.commit()

            flash('an empty collection added - please add cards!!', category = 'success')

    return render_template('home.html', user = current_user) 


@views.route('/play-collection/<id>', methods=['GET','POST'])
def play_coll(id):
    collection = Collection.query.get(id)
    if request.method == 'GET':
        return render_template('play.html', collection = collection,user = current_user )
    elif request.method == 'POST':
        return render_template('play.html', collection = collection,user = current_user )


@views.route('/edit-collection/<id>', methods=['GET','POST'])
def edit_coll(id):
    collection = Collection.query.get(id)
    if request.method == 'GET':
        print("Hi there")
        return render_template('edit_collection.html', collection = collection,user = current_user  )
    elif request.method == 'POST':
        question =  request.form.get('question')
        answer = request.form.get('answer')
        new_card = Card(question = question, answer = answer, collection_id = collection.id)
        db.session.add(new_card)
        db.session.commit()
        return render_template('edit_collection.html', collection = collection,user = current_user ) 


@views.route('/delete-coll', methods=[ 'POST'])
def delete_coll():
    data = json.loads(request.data)
    collId = data['collId']
    #print(collId)
    collection = Collection.query.get(collId)
    #print(collection.name)
    if collection:
        #print("yes man")
        if collection.user_id == current_user.id:
            #print("hello")
            db.session.delete(collection)
            db.session.commit()
    return jsonify({})

#@views.route('/edit_collection', methods=['POST']) 
#def edit_collection(id):
#    collection = Collection.query.get(id) 
#    return render_template("edit_collection.html", collection)
    
@views.route('/delete-card', methods=[ 'POST'])
def delete_card():
    data = json.loads(request.data)
    cardlId = data['cardlId']
    #print(collId)
    card = Card.query.get(cardlId)
    collection = Collection.query.get(card.collection_id)
    #print(collection.name)
    if card:
        #print("yes man")
        if collection.user_id == current_user.id:
            #print("hello")
            db.session.delete(card)
            db.session.commit()
    return jsonify({})


