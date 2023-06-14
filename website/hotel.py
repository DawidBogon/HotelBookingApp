#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import WebsiteHotel
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import datetime
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

    if request.method == 'POST':
        reservation_start = request.form.get('reservation_start')
        reservation_end = request.form.get('reservation_end')

        if reservation_start < reservation_end:
            # sprawdzanie rezerwacji dla danego pokoju, czy jest wolne
            room_transactions = website.Transaction.query.filter(website.Transaction.room == room_id).all()
            if room_transactions:
                not_reserved_flag = True
                for transaction in room_transactions:
                    room_reservation = website.Reservation.query.filter(website.Reservation.transaction == transaction.id)[0]
                    res_start = datetime.strptime(reservation_start, '%Y-%m-%d')
                    res_end = datetime.strptime(reservation_end, '%Y-%m-%d')
                    not_reserved_flag = not_reserved_flag and ((room_reservation.reservation_start < res_start and room_reservation.reservation_end < res_start) or (room_reservation.reservation_start > res_end and room_reservation.reservation_start > res_end))
                if not_reserved_flag:
                    create_transaction(room_id, reservation_start, reservation_end)
                else:
                    flash('This date is unavailable', category='error')
            else:
                create_transaction(room_id, reservation_start, reservation_end)
        else:
            flash('Incorrect date range', category='error')
    room = website.Room.query.get_or_404(room_id)
    return render_template('hotel.html', room=room)


def create_transaction(room_id, reservation_start, reservation_end):
    user_id = session.get('user_id')
    new_transaction = website.Transaction(user=user_id, room=room_id)
    website.db.session.add(new_transaction)
    website.db.session.commit()
    website.db.session.refresh(new_transaction)
    new_reservation = website.Reservation(transaction=new_transaction.id,
                                          reservation_start=reservation_start,
                                          reservation_end=reservation_end,
                                          canceled=False)
    website.db.session.add(new_reservation)
    website.db.session.commit()
    flash('Reservation done succesfully!', category='success')
