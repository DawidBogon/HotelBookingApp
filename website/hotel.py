#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2.errors

from . import WebsiteHotel
from flask import Blueprint, render_template, request, flash, make_response, jsonify
from datetime import datetime
import time
from sqlalchemy.sql import text
hotel = Blueprint('hotel', __name__)

website = WebsiteHotel()


@hotel.route('/<int:room_id>', methods=['GET', 'POST'])
def reservation(room_id):
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    user_id = request.args.get('user_id')

    if request.method == 'POST':
        session = website.Session()
        try:
            session.execute(text('LOCK TABLE rooms IN EXCLUSIVE MODE;'))
            room_reservations = session.query(website.Reservation).filter(website.Reservation.room == room_id).all()
            reservation_start = request.form.get('reservation_start')
            reservation_end = request.form.get('reservation_end')

            if reservation_start < reservation_end:
                not_reserved_flag = True
                for reservation in room_reservations:
                    res_start = datetime.strptime(reservation_start, '%Y-%m-%d')
                    res_end = datetime.strptime(reservation_end, '%Y-%m-%d')
                    not_reserved_flag = not_reserved_flag and (
                                (reservation.reservation_start < res_start and reservation.reservation_end < res_start) or (
                                    reservation.reservation_start > res_end and reservation.reservation_start > res_end))
                if not_reserved_flag:
                    create_transaction(room_id, reservation_start, reservation_end, user_id, first_name, last_name, session)
                else:
                    flash('This date is unavailable', category='error')
            else:
                flash('Incorrect date range', category='error')
            session.commit()
        except:
            session.commit()
    room_reservations = website.Reservation.query.filter(website.Reservation.room == room_id).all()
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


def create_transaction(room_id, reservation_start, reservation_end, user_id, first_name, last_name, session):
    new_reservation = website.Reservation(user_id=user_id,
                                          first_name=first_name,
                                          last_name=last_name,
                                          room=room_id,
                                          reservation_start=reservation_start,
                                          reservation_end=reservation_end,
                                          canceled=False)
    session.add(new_reservation)
    # time.sleep(5)
    flash('Reservation done successfully!', category='success')

