#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import WebsiteHotel
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response, jsonify
from datetime import datetime
from sqlalchemy.orm.exc import StaleDataError
import requests
hotel = Blueprint('hotel', __name__)

website = WebsiteHotel()


@website.login_manager.user_loader
def load_user(user_id):
    return website.User.query.get(int(user_id))


@hotel.route('/<int:room_id>/', methods=['GET', 'POST'])
def reservation(room_id):
    # TODO - add verification if user is logged in
    # if not session.get('logged_in'):
    #     flash('You need to login first.', category='success')
    #     session['prev_url'] = url_for('/', room_id=room_id)
    #     return redirect(url_for('auth.login'))
    room_reservations = website.Reservation.query.filter(website.Reservation.room == room_id).all()
    if request.method == 'POST':
        reservation_start = request.form.get('reservation_start')
        reservation_end = request.form.get('reservation_end')

        if reservation_start < reservation_end:
            # sprawdzanie rezerwacji dla danego pokoju, czy jest wolne
            not_reserved_flag = True
            for reservation in room_reservations:
                res_start = datetime.strptime(reservation_start, '%Y-%m-%d')
                res_end = datetime.strptime(reservation_end, '%Y-%m-%d')
                not_reserved_flag = not_reserved_flag and (
                            (reservation.reservation_start < res_start and reservation.reservation_end < res_start) or (
                                reservation.reservation_start > res_end and reservation.reservation_start > res_end))
            if not_reserved_flag:
                create_transaction(room_id, reservation_start, reservation_end)
            else:
                flash('This date is unavailable', category='error')

        else:
            flash('Incorrect date range', category='error')
    room = website.Room.query.get_or_404(room_id)
    return render_template('hotel.html', room=room, room_reservations=room_reservations)


@hotel.route('/get_all_rooms', methods=['GET'])
def get_all_rooms():
    rooms = website.Room.query.all()
    res_table = []
    for room in rooms:
        res_table.append(room.return_table())

    response = make_response(jsonify(res=res_table))
    response.headers["Content-Type"] = "application/json"
    return response


def create_transaction(room_id, reservation_start, reservation_end):
    user_id = session.get('user_id')
    try:
        new_reservation = website.Reservation(user=user_id,
                                              room=room_id,
                                              reservation_start=reservation_start,
                                              reservation_end=reservation_end,
                                              canceled=False)
        website.db.session.add(new_reservation)
        website.db.session.commit()
        flash('Reservation done succesfully!', category='success')
    except StaleDataError:
        flash('Reservation failed', category='fail')

