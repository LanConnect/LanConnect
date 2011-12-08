# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User

from models import *

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name']

class EntrantAdmin(admin.ModelAdmin):
	list_display = ['team_name', 'skill', 'location']

class GameAdmin(admin.ModelAdmin):
	list_display = ['name']

class EventAdmin(admin.ModelAdmin):
	list_display = ['name', 'start', 'end', 'location', 'organiser', 'in_progress']

class StationAdmin(admin.ModelAdmin):
	list_display = ['name', 'event']
	filter_vertical = ['games']

class TournamentAdmin(admin.ModelAdmin):
	list_display = ['name', 'start', 'end', 'event']
	#list_display_links = ['event']
	filter_vertical = ['entrants']

#class MatchAdmin(admin.ModelAdmin):
#	list_display = ['tournament_game', 'winner', 'started', 'finished']

for m, a in (
	(Location, LocationAdmin),
	(Entrant, EntrantAdmin),
	(Game, GameAdmin),
	(Event, EventAdmin),
	(Station, StationAdmin),
	(Tournament, TournamentAdmin),
#	(Match, MatchAdmin),
):
	admin.site.register(m, a)

