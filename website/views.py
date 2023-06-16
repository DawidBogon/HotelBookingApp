#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
import json
from . import WebsiteUser
import requests

views = Blueprint('views', __name__)

website = WebsiteUser()


@views.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        flash('You need to login first.', category='success')
        session['prev_url'] = url_for('views.home')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = website.TestTable(data=note)
            website.db.session.add(new_note)
            website.db.session.commit()
            flash('Note added!', category='success')

    table = website.TestTable.query.all()

    return render_template("home.html", table=table, user=session.get('logged_in'))


@views.route('/search-room', methods=['GET', 'POST'])
def search_room():
    if request.method == 'POST':
        city = request.form.get('city', None)
        hotel_name = request.form.get('price', None)
        min_rating = request.form.get('min_rating', None)
        max_rating = request.form.get('max_rating', None)
        no_of_beds = request.form.get('no_of_beds', None)
        names = ['city', 'price', 'min_rating', 'max_rating', 'no_of_beds']
        values = [city, hotel_name, min_rating, max_rating, no_of_beds]
        payload = {names[it]: value for it, value in enumerate(values) if value is not None}
        res = requests.post('http://localhost:5001/get-rooms', json=payload)
        if res.status_code == 200:
            rooms = res.json()
            if len(rooms['res']) > 0:
                flash('Found Rooms', category='info')
                return render_template("rooms_list.html", user=session.get('logged_in'),
                                       rooms=rooms['res'], last_name=session.get('last_name'),
                                       first_name=session.get('first_name'), user_id=str(session.get('user_id')))
            else:
                flash('There are no rooms', category='error')
            return render_template("search.html", user=session.get('logged_in'))
        else:
            flash(f'Invalid response {res.status_code}', category='error')
    return render_template("search.html", user=session.get('logged_in'))


@views.route('/delete-entry', methods=['POST'])
def delete_entry():
    entry = json.loads(request.data)
    entryId = entry['entryId']
    entry = website.TestTable.query.get(entryId)

    print(entry)

    if entry:
        website.db.session.delete(entry)
        website.db.session.commit()

    return jsonify({})
