#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, jsonify
import json
from . import Website

views = Blueprint('views', __name__)

website = Website()

@views.route('/', methods=['GET', 'POST'])
def home():
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

    return render_template("home.html", table=table)


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
