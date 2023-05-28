#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
import json
from . import WebsiteUser

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
