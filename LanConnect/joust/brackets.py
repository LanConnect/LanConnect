import math
from models import Match, Tournament
from django.db import transaction

#single elimination generator
@transaction.commit_on_success()
def generate_se(tournament):
	tournament = Tournament.objects.select_related().get(pk=tournament.pk)
	tournament.matches.all().delete()
	
	entrants_per_match = tournament.entrants_per_match
	num_players = tournament.entrants.count()
	if tournament.bracket_type != 'se':
		raise ValueError('needs tournament with single elimination style')
	if num_players < entrants_per_match:
		raise ValueError('needs at least 2 or more entrants.')
	
	if tournament.seed_type == 'r':
		entrants = list(tournament.entrants.all().order_by('?')) # force queryset evaluation
	else:
		raise NotImplementedError('only random is implemented')
	
	num_rounds = int(math.ceil(math.log(num_players, entrants_per_match)))
	byes = entrants_per_match**num_rounds - num_players
	
	#wrap this in a transaction
	### Generate Bracket ###
	final_match = Match(tournament_game=tournament)
	final_match.save()
	tournament.root_match = final_match
	print "created root object"
	
	rounds = [[final_match]]
	
	#iterate backward through rounds
	for round in xrange(1, num_rounds):
		print "level %i" % round
		prev_level = rounds[round-1]
		this_round = []
		for match in prev_level:
			for slot in xrange(entrants_per_match):
				m = Match(tournament_game=tournament)
				m.winner_next = match
				m.save()
				print "slot %i" % slot
				this_round.append(m)
		rounds.append(this_round)
	
	#seed first round
	half = int(math.ceil(entrants_per_match/2))
	for match in rounds[num_rounds-1]:
		if byes > half: # set up first round byes
			for slot in xrange(entrants_per_match-half):
				seed_match(tournament, match, entrants)
			byes -= half
		else: # clean up remaining byes
			for slot in xrange(entrants_per_match-byes):
				seed_match(tournament, match, entrants)
			byes = 0
		print "seeded: %s" % match
	
	#put code for double elim here
	
	#prune any rounds with too few people to start
	for match in rounds[num_rounds-1]:
		if match.entrants.count() == 1:
			print "prune: %s" % match
			for e in match.entrants.all():
				match.winner_next.entrants.add(e)
			match.delete()
	
def seed_match(tournament, match, entrants):
	# keep players sorted together together
	if tournament.seed_type in ['s', 'n', 'r']:
		match.entrants.add(entrants.pop(0))
	
	# keep players sorted together apart
	# sample top-center to avoid playing
	# the best player against the worst
	if tournament.seed_type in ['d', 'f']:
		if not slot%2:
			match.entrants.add(entrants.pop(0))
		else:
			match.entrants.add(entrants.pop(len(entrants)))
