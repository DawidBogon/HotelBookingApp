#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import WebsiteHotel
from flask import Blueprint, render_template, request, flash, redirect, url_for

hotel = Blueprint('hotel', __name__)

website = WebsiteHotel()


@website.login_manager.user_loader
def load_user(user_id):
    return website.User.query.get(int(user_id))


@hotel.route('/<int:room_id>/')
def get_hotel_room(room_id):
    room = website.Room.query.get_or_404(room_id)
    return render_template('hotel.html', room=room)

