#django framework
from django import forms as djforms
from django.conf import settings
from django.shortcuts import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#joust
import models, forms
#library functions
from gettext import gettext as _
from datetime import datetime
from xml.dom.minidom import parse

def tio(request):
	return render_to_response('joust/tio.html', {'import_f': TioImportForm()}) 

def tio_import(request):
	if request.method != 'POST':
		raise Exception("method not allowed")
	form = TioImportForm(request.POST, request.FILES)
	if form.is_valid():
		f = request.FILES['file']
		if f.size > 10485760:
			raise Exception, "file is greater than 10MB.  not attempting to process"
		msgs = ""
		
		# attempt to load into the dom
		msgs += 'Loading XML (%s bytes)\n' % f.size
		document = parse(request.FILES['file'])
		msgs += 'XML parsed\n'
		msgs += str(dir(document))
		
		
		return render_to_response('joust/tio/tio.import.html', {'msgs': msgs})
	else:
		return render_to_response('joust/tio/tio.html', {'import_f': form})

def event_picker(request):
	running_events =  models.Event.objects.filter(in_progress=True)
	upcoming_events = models.Event.objects.filter(in_progress=False, end__gt=datetime.now())
	
	return render_to_response('joust/mobile/events.html', 
								{'running_events':running_events,
								 'upcoming_events':upcoming_events}, 
								context_instance=RequestContext(request))
	
# User self service signups ----------------------------------------------------------------------
def user_signup(request):
	if request.user.is_authenticated():
		return redirect('joust-selfserve-tournament')
	#process form
	if request.POST:
		signupform = forms.UserSignupForm(request.POST)
		if signupform.is_valid():
			if not User.objects.filter(username=signupform.cleaned_data['handle']).count():
				u = User(
						username=signupform.cleaned_data['handle'],
						email=signupform.cleaned_data['email'],
						first_name=signupform.cleaned_data['first_name'],
						last_name=signupform.cleaned_data['last_name'],
					)
				u.set_unusable_password()
				u.save()
				try:
					if settings.JOUST_SMS_NOTIFICATIONS == True:
						p = u.get_profile()
						p.phone_number = signupform.cleaned_data['phone_number']
				except:
					pass
				login(request, u)
				return redirect('joust-selfserve-tournament')
			else:
				signupform._errors['handle'] = _(u'This handle has been taken.')
				
	#generate blank form
	else:
		signupform = forms.UserSignupForm()
		
	return render_to_response('joust/self-service/signup.html', {'signupform':signupform}, 
								context_instance=RequestContext(request))

@login_required
def user_tournament(request):
	if request.POST:
		tournamentform = forms.UserTournamentForm(request.POST )
		if tournamentform.is_valid():
			pass
	else:
		tournamentform = forms.UserTournamentForm()
	return render_to_response(
		'joust/self-service/tournaments.html',
		{'tournamentform':tournamentform},
		context_instance=RequestContext(request)
	)

def user_confirm(request):
	pass

# Admin/organizer views ------------------------------------------------------------

@login_required
def admin_splash(request):
	
	return render_to_response('joust/admin/start.html', {}, 
								context_instance=RequestContext(request))
	
@login_required
def admin_signup(request):
	if request.user.is_staff:
		signupform = forms.UserSignupForm(request.POST)
	
	return render_to_response('joust/admin/signup.html', {}, 
		context_instance=RequestContext(request))

@login_required
def generate_bracket(request):
	if request.user.is_staff or request.user.has_perm('tournamentgame.can_generate_bracket'):
		if request.POST:
			bracketform = forms.BracketGenerationForm(request.POST)
			if bracketform.is_valid():
				raise ValueError("Everything went better than expected :D")
		else:
			bracketform = forms.BracketGenerationForm()
			
		return render_to_response('joust/admin/tournaments/bracket_gen.html', {'bracketform':bracketform}, 
			context_instance=RequestContext(request))
		
	return redirect('joust.admin.splash')

@login_required
def create_tournament(request):
	if request.user.is_staff or request.user.has_perm('tournamentgame.can_add'):
		if request.POST:
			tournamentform = forms.CreateTournamentForm(request.POST)
			tournamentform.instance.event = models.Event.objects.get(in_progress=True)
			if tournamentform.is_valid():
				tournamentform.save()
				return redirect('joust-start')
		else:
			tournamentform = forms.CreateTournamentForm()
		print tournamentform
		return render_to_response('joust/admin/tournaments/create.html', {'tournamentform': tournamentform},
			context_instance=RequestContext(request))
	return redirect('joust-admin-splash')

def helper_match(request, station_id):
	station = get_object_or_404(models.Station, id=station_id)
	
	return render_to_response('joust/admin/tournaments/create.html', 
							{'station': station},
		context_instance=RequestContext(request))

def user_select(request):
	#Will map to the ManageUserForm
	pass

def user_tournament_manage(request):
	#will map to our ModifySignupForm
	pass

def edit_tournament(request):
	#Will map to our tournament editing form
	pass
		
# Station Administration ---------------------------------------------------------------
def pick_station(request):
	stations = models.Station.objects.all()
	
	return render_to_response('joust/display/projector.html',
								{'stations':stations,},
								context_instance=RequestContext(request))

# Bracket and Tournament Display -------------------------------------------------------
def tournament_show_bracket(request, tournament_game_id):
	tournament_game = get_object_or_404(models.Tournament, id=tournament_game_id)
	
def display_projector(request):
	
	return render_to_response('joust/display/projector.html', {}, 
								context_instance=RequestContext(request))
	
def display_hdtv(request):
	tournament = models.Tournament.objects.all()[0]
	root_match = tournament.matches.filter(winner_next=None, runner_up_next=None)[0]
	
	return render_to_response('joust/display/hdtv.html', {'area': 'default', 'root_match':root_match}, 
								context_instance=RequestContext(request))
	
def display_phone(request):
	tournaments = models.Tournament.objects.all().order_by('start')
	event = models.Event.objects.all()[0]
	
	return render_to_response('joust/display/phone.html', {
									'area': 'default',
									'event':event,
									'tournaments':tournaments 
								}, context_instance=RequestContext(request))
	
