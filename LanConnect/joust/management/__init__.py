from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import signals, get_apps, get_models
from django.contrib.auth.models import User
from LanConnect.joust.models import Location, Event, Entrant, Game, Station, Tournament, Match
from LanConnect.joust import models

@transaction.commit_on_success()
def init_data(app, created_models, verbosity, **kwargs):
	"""
	This code ONLY TRIGGERS if you actually drop ALL the tables from joust.  If you do partial things,
	manage.py reset commands, or other things, it DOESN'T ACTUALLY ACTIVATE.
	
	Likewise, this code WILL NOT RUN if you do not create all models for the app at once.
	"""
	if Event in created_models:
		e = Event(
			name="Test Event",
			start=datetime.now() - timedelta(hours=5),
			end=datetime.now() + timedelta(days=2),
			location="Example Convention Centre",
			organiser="Sample Videogaming Association, Example Arcade Society",
			in_progress=True
		)
		e.save()
		
		if Location in created_models:
			l = Location(name='Example Location')
			l.save()
			
			if Entrant in created_models:
				for i in xrange(14):
					u = User(
						username='example%s' % i,
					)
					u.save()
					
					en = Entrant(
						team_name='Example Entrant %i' % i,
						event=e,
						location=l,
						primary_user=u,
					)
					en.save()
					
				if Game in created_models:
					g = Game(
						name='Super Example Bros. (tm)',
						platform='X' # this is a single character platform code, not a full string.
					)
					g.save()
					
					if Station in created_models:
						s = Station(
							name='Station 1',
							event=e
						)
						s.save()
						s.games.add(g)
						#created Station
						
						if Tournament in created_models:
							t = Tournament(
								name="Example Tournament",
								start=datetime.now()-timedelta(hours=2),
								end=datetime.now()+timedelta(hours=1),
								event=e,
								max_entrants=16,
								game=g
							)
							t.save()
							
							for en in Entrant.objects.filter(event=e):
								t.entrants.add(en)
							print " --- Created initial data for joust!"

signals.post_syncdb.connect(init_data, sender=models, dispatch_uid="LanConnect.joust.management.init_data")