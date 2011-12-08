"""
LanConnect/booking/py - Models for seat booking
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

from django.db.models import *
from django.contrib.auth.models import Group
#from django.conf import settings
from events.models import Event

TICKETS = (
    ('a', 'Allocated'),
    ('s', 'Social'),
)

POLICY = (
    ('a', 'Allow',),
    ('d', 'Deny',),
)

class Venue(Model):
    name = CharField(max_length=60)
    location = TextField()
    floorplan = ImageField(upload_to="booking/floorplans")
    seat_size = IntegerField()
    
class SeatAttribute(Model):
    name = CharField(max_length=20, help_text="Moniker (i.e. 'Admin' for Admin only seating)")
    
class Seat(Model):
    venue = ForeignKey(Venue)
    name = CharField(max_length=10)
    attributes = ManyToManyField(SeatAttribute)
    x = IntegerField()
    y = IntegerField()

#todo: needs lambdas
class SeatingPolicy(Model):
    policy = CharField(max_length=1,choices=POLICY)
    attribute = ForeignKey(SeatAttribute)
    group = ForeignKey(Group)
    reason = TextField(null=True, blank=True)

class Modifier(Model):
    name = TextField()

class Attendance(Model):
    event = ForeignKey(Event)
    user = ForeignKey(User)
    seat = ManyToManyField(null=True, help_text='Seat ID')
    modifiers = ManyToManyField(Modifier)
    ticket = CharField(choices=TICKETS, help_text='Ticket Type:')
    
class Ban(Model):
    user = ForeignKey(User)
    start = DateField(auto_now=True)
    end = DateField()
    given_by = ForeignKey(User)
    reason = TextField()
    