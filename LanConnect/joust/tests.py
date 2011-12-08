
from django.test import TestCase
from models import *
from django.contrib.auth.models import *
from datetime import timedelta, datetime

def generate_test_data():
	# Generate an event to store the games.
	evt = Event(
		name="Test Tournament",
		start=datetime.now() - timedelta(hours=5),
		end=datetime.now() + timedelta(days=2),
		location="Example Convention Centre",
		organiser="Sample Videogaming Association, Example Arcade Society",
		in_progress=True
	)
	evt.save()
	
	# generate a game
	game = Game(
		name="Super Smash Brothers Brawl",
		platform="I"
	)
	game.save()
	
	# generate some stations
	stations = []
	for x in range(1,6):
		station = Station(
			name="Brawl %s" % x,
			event=evt
		)
		station.save()
		
		station.games.add(game)
		
		station.save()
		stations.append(station)
	
	# generate a tournament game
	tg = Tournament(
		name="Brawl 1v1",
		start=datetime.now() - timedelta(hours=1),
		end=datetime.now() + timedelta(hours=3),
		event=evt,
		max_entrants=16,
		game=game
	)
	
	tg.save()
