# -*- coding: utf-8 -*-
from django.db.models import *
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from gettext import gettext as _
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

# Different bracket types that may be used for a tournament.
BRACKET_TYPES = (
	('se', 'Single Elimination'),
	('de', 'Double Elimination'),
	('rr', 'Round Robin'),
)

# is it a single person per bracket or team/clan play?
PLAY_TYPES = (
	('s', 'Solo event'),
	('t', 'Team event'),
)

# This defines various policies that we can use for seeding a competition.
SEED_TYPES = (
	('r', 'Random'),
	('s', 'Same-skilled together'),
	('d', 'Differently-skilled together'),
	('n', 'Same-location together'),
	('f', 'Different-location together'),
)

# the database structure here is inspired a lot by TIO, so a lot of the
# concepts used in that program are similar.  this should also allow you
# to easily import/export a tio file.
#
# it does however extend on some concepts.

class Location(Model):
	class Meta:
		ordering = ['name']
	name = CharField(max_length=256, help_text="The hometown or region's name.  Locations can be as specific (town) or broad (state) as you like.")
	
	def __unicode__(self):
		return self.name

class Event(Model):
	class Meta:
		ordering = ['start', 'name']
		
	name = CharField(max_length=64)
	start = DateTimeField()
	end = DateTimeField()
	
	location = CharField(max_length=128, blank=True)
	organiser = CharField(max_length=256, blank=True)
	in_progress = BooleanField(blank=True)
	
	def __unicode__(self):
		return self.name

class Entrant(Model):
	"""
	Defines an entrant to the tournament.  An entrant may be either an individual
	or a team - it doesn't matter in the context of our program.  We *assume* that
	everyone is a team, that can map to 0 or more actual user accounts.  In the
	end Joust doesn't really care how it all maps up to a real-world scenario.
	
	Each entrant in a sense is like a ticket, but not quite.  Entrance is done on
	a per-event basis.  What this means is that a team with the same name can
	have different members at two different events.
	"""
	class Meta:
		ordering = ['team_name', 'primary_user__username']
	
	team_name = CharField(
		max_length=256,
		help_text=u"If this is a team, you should write their name here.",
		blank=True
	)
	
	skill = SmallIntegerField(
		help_text=u"Used to determine the relative skills of players, which may be "+
			u"used when developing a bracket. 0 is 'normal', negative values "+
			u"mean less skilled players, positive values mean more skilled "+
			u"players.  Use whole numbers.",
		default=0
	)
	
	event = ForeignKey(
		"Event",
		help_text=u"The event that this person or team is an entrant in."
	)
	
	location = ForeignKey(
		Location,
		null=True,
		blank=True,
		help_text=u"Used to indicate the hometown/region of the player, which may "+
			u"be used when developing a bracket."
	)
	
	primary_user = ForeignKey(
		User,
		related_name="_tournament_primary_user",
		help_text=u"The primary user that this entrance is associated with.  In "+
			u"the context of an individual, this is their user account.  In "+
			u"the context of a team, this is the team's captain."
	)
	
	members = ManyToManyField(
		User,
		related_name='tournament_entries',
		blank=True,
		help_text=u"User(s) that are associated with this entry (optional).  This "+
			u"can be used to grant authenticated access to certain parts of "+
			u"the system for participants."
	)
	
	photo = ImageField(
		blank=True,
		upload_to='entrant_photos',
		help_text="Used to publicly identify various entrants.  Depending on your tournament, this could be a photo or it could be an avatar."
	)
	
	confirmed = BooleanField( default=False )
	
	def is_team(self):
		if self.members.all().count():
			return True
		else:
			return False
	is_team.boolean=True
	
	def is_individual(self):
		return not self.is_team()
	is_individual.boolean=True
		
	def __unicode__(self):
		if self.team_name:
			if self.primary_user.username:
				return u"%s (%s)" % (self.team_name, self.primary_user.username)
			else:
				return self.team_name
		elif self.primary_user.username:
			return self.primary_user.username

# also the game. 
class Game(Model):
	"""Defines the names of various games that may be played."""
	class Meta:
		ordering = ['name']
	
	name = CharField(max_length=256)
	
	platform = CharField(
		max_length=32,
		help_text=u"The platform code for this game, corresponding to Console Logos font.",
		blank=True
	)
	
	def __unicode__(self):
		return self.name
		
	@permalink
	def get_absolute_url(self):
		return ('game_detail', (), dict(object_id=self.id))
		

class Station(Model):
	class Meta:
		ordering = ['name']

	name = CharField(max_length=64)
	games = ManyToManyField(Game, help_text="The games that may be played at this station. If this is left blank, then all games may be played here.")
	event = ForeignKey(Event)
	
	def __unicode__(self):
		return self.name
	
	def current_match(self):
		"Look up what game is being played at this station right now.  In an 'ideal' situation, there will be 0 or 1 matches being played."
		return Match.objects.exclude(
				started_exact=None,  #exclude queued matches
			).get(
				finished_exact=None,
				station=self,)
	
	def next_match(self):
		return Match.objects.get(
				started_exact=None,
				station=self,)
		
	def get_potential_matches(self):
		return Match.objects.filter(station__exact=None,
					tournament__game__in=self.games,) # is this station capable?
				
		
	def available(self):
		return not self.current_match().exists()
	available.boolean = True
	
	
class Tournament(Model):
	"""Defines a tournament game"""
	class Meta:
		ordering = ['start', 'name']
		verbose_name = 'tournament'
		verbose_name_plural = 'tournaments'
		permissions = (
					('can_generate_bracket', "User has permission to generate brackts for a tournament."),
					)
	
	name = CharField(
		max_length=256,
		help_text=u"The name of this tournament game.  For example, “Brawl FFA”, “ExampleCo Entertainment Street Fighter Challenge”."
	)
	
	#listed start and end time
	start = DateTimeField(
		help_text=u"The start time of this tournament game."
	)
	end = DateTimeField(
		help_text=u"The end time of this tournament game."
	)
	
	#recorded start and end times
	started_at = DateTimeField(
		null=True,
		blank=True,
		help_text=u"The time that this tournament started. If set to None, then the tournament has not started"
	)
	finished_at = DateTimeField(
		null=True,
		blank=True,
		help_text=u"The time that this tournament finished.  If set to None, then the game is still in progress."
	)
	
	game = ForeignKey(Game)
	
	event = ForeignKey(
		Event,
		related_name = 'tournaments_run',
		help_text=u"The event that this tournament game is played at."
	)
	seed_type = CharField(
		max_length=1,
		choices=SEED_TYPES,
		default="r",
		help_text=u"Which seeding policy should be used for generating the bracket for this tournament?"
	)
	
	bracket_type = CharField(max_length=2, choices=BRACKET_TYPES, default="se")
	max_entrants = PositiveIntegerField(
		blank=True,
		null=True,
		help_text=u"(Optional) The maximum number of entrants in the tournament.  It is recommended that you make this a power of 2.  (2, 4, 8, 16, 32...)"
	)
	
	entrants = ManyToManyField(
		Entrant,
		null=True,
		blank=True,
		help_text=u"The entrants in the tournament."
	)
	
	# define how to seed these matches
	players_per_entrant = PositiveIntegerField(
		default=1,
		help_text=u"The number of players that are in each entrant for this tournament (the size of the team).  For a 1v1, this is 1, for a 2v2 and 2v2v2, this is 2, for a 4-player FFA (1v1v1v1), this is 1."
	)
	
	entrants_per_match = PositiveIntegerField(
		default=2,
		help_text=u"The number of entrants that are in each game for this tournament (the number of teams per game).  For a 1v1 and 2v2, this is 2, for 2v2v2 this is 3, for a 4-player FFA (1v1v1v1), this is 4."
	)
	
	game = ForeignKey(
		Game,
		related_name = 'tournament_games',
		help_text=u"The game that is being played.",
	)
	root_match = ForeignKey(
		'Match',
		null=True,
		related_name="_root_tournament",
		editable=False,
	)
	def can_start(self):
		return datetime.now() > self.start
	def in_progress(self):
		return (self.started_at and self.finished_at == None)
	in_progress.boolean = True
	def has_finished(self):
		return bool(self.finished_at)
	
	def startable_matches(self):
		return self.matches.filter(start__gt=datetime.now())
	def in_progress_matches(self):
		return self.matches.filter(finished_at__exact=None).exclude(started_at__exact=None)
	
	
	def __unicode__(self):
		return "%s (%s)" % (self.name, self.start.strftime('%A %H:%M'))
	
	#def matches(self):
	#    return Match.objects.filter(tournament_game__id=self.id)
		
	@permalink
	def get_absolute_url(self):
		return ('tournament_detail', (), dict(object_id=self.id))
	
class Match(Model):
	"""Defines a match in a bracket"""
	class Meta:
		verbose_name_plural = "matches"
	
	tournament = ForeignKey(Tournament, related_name='matches')
	entrants =   ManyToManyField(Entrant, related_name="_matches_entered")
	#when station attribute is set, match is no longer available for queuing
	station =    ForeignKey(Station, related_name="_matches_played", null=True, blank=True, help_text="The station that this game was played on, or the one that this it so be played on.")
	
	winner =     ForeignKey(Entrant, null=True, help_text="The winner of the match", related_name='_matches_won')
	runner_up =  ForeignKey(Entrant, null=True, help_text="Runner up of the match", related_name='_matches_placed')
	
	winner_next =    ForeignKey('self', null=True, help_text="The winner goes to this match", related_name='from_winner')
	runner_up_next = ForeignKey('self', null=True, help_text="The runner_up goes to this match", related_name='from_runner_up')
	
	announced =  DateTimeField(null=True, blank=True, help_text="The time the game was announced to participants. Game cannot start for certain period after announcement.")
	started =    DateTimeField(null=True, blank=True, help_text="The time the game has started. If not blank, then the game has started.")
	finished =   DateTimeField(null=True, blank=True, help_text="The time the game has finished. If not blank, then the game has finished.")
	
	def can_start(self):
		if not self.from_winner.exclude(finished=None).count():
			return False
		if not self.from_runner_up.exclude(finished=None).count():
			return False
		if self.entrants.count() < 2:
			return False
		if self.can_start_at() < datetime.now():
			return False
		return True
	
	def can_start_at(self):
		return self.announced + timedelta(**settings.MATCH_GRACE_PERIOD)
	
	def in_progress(self):
		if self.started and not self.finished:
			return True
		return False
	
	def __unicode__(self):
		if not self.entrants.count() < 2:
			return " v.s. ".join([unicode(entrant) for entrant in self.entrants])
		else:
			return " new event for %s" % unicode(self.tournament)

class Result(Model):
	""" bridges between match and entrant to record rankings/scores for a match. """
	
	TYPE_CHOICES = (
		('f', 'Forfeit'),
		('d', 'Disqualified'),
	)
	
	entrant = ForeignKey(Entrant)
	match   = ForeignKey(Match)
	special = CharField(max_length=1, choices=TYPE_CHOICES, null=True)
	score   = IntegerField(help_text=_("For scored matches, the score of the attendee. For knockout matches the order of players."))
	