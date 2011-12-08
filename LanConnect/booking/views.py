"""
LanConnect/booking/models.py - Views for seat booking
Copyright 2010 Thomas Woolford

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy

from django.forms import forms
from django.forms import HiddenInput
from django.shortcuts import render_to_response

from events.models import Event
from models import LanBooking

SEAT_LIST = [
             {'id':1, 'x':0, 'y':0},
             {'id':2, 'x':30, 'y':0},
            ]


class BookingForm(forms.Form):
    class Meta:
        model = LanBooking
        fields = ['seat', 'food', 'ticket',]
        widgets = {'seat': HiddenInput(),}
        
def booking_form(request):
    #make sure that we have a lan coming up
    event = Event.objects.filter(categories__name__icontains='lan').latest('start')
    if not event:
        raise ValueError
    
    bookingform = BookingForm(initial={'user':request.user, 'event': event,})
    bookings = list(LanBooking.objects.filter(event=event).all())
    
    #populate seats
    seats = copy.deepcopy(SEAT_LIST)
    for booking in bookings:
        for seat in seats:
            if seat.id == booking.seat.pk:
                seat['user'] = booking.user
    
    return render_to_response("bookings/seating.html", {"event":event, "bookingform": bookingform, "seats":seats,})