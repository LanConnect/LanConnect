from os.path import dirname, abspath, join
from django.conf.urls.defaults import *
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from models import *
import views

games_qsd = dict(queryset = Game.objects.all())
tournament_qsd = dict(queryset=Tournament.objects.filter(event=Event.objects.get(in_progress=True)))

urlpatterns = patterns('',
	url('^$', lambda request: redirect(reverse('joust-start')), name='joust-index'),
	
	# games
	url(r'^games/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', dict(games_qsd), name='joust-game_detail'),
	
	# tournaments
	url(r'^tournament/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(tournament_qsd), name='joust-tournament_detail'),
	url(r'^tournament/(?P<tournament_game_id>\d+)/bracket/$', views.tournament_show_bracket, name='joust-tournament_show_bracket'),
	
	#start page
	url(r'^start$', 'django.views.generic.simple.direct_to_template', {'template':'joust/start.html'}, name='joust-start'),
	
	# user_self-service system
	url(r'^self-service/signup$', views.user_signup, name='joust-selfserve-signup'),
	url(r'^self-service/tournament$', views.user_tournament, name='joust-selfserve-tournament'),
	url(r'^self-service/confirm$', views.user_confirm, name='joust-selfserve-confirm'),
	
	# organiser functionality
	url(r'^admin$', views.admin_splash, name='joust-admin-index'),
	url(r'^admin/tournament/gen_bracket$', views.generate_bracket, name='joust-admin-tournaments-gen_bracket'),
	url(r'^admin/tournament/create$', views.create_tournament, name='joust-admin-tournaments-create_tournament'),
	
	# helper system
	url(r'^helper/match/(?P<matchid>\d+)', views.helper_match, name='joust-helper-match'),
	url(r'^helper/events$', views.event_picker, name="joust-helper-event_picker"),
	url(r'^helper/tournaments$', 'views.tournament_picker', name="joust-helper-tournament_picker"),
	
	#tio import
	url(r'^admin/import/tio.form$', views.tio, name='joust.admin.tio.form'),
	url(r'^admin/import/tio.import$', views.tio_import, name='joust.admin.tio.import'),
	
	#display methods
	url(r'^display/projector$', views.display_projector, name='joust-display-projector'),
	url(r'^display/hdtv$', views.display_hdtv, name='joust-display-hdtv'),
	url(r'^display/phone$', views.display_phone, name='joust-display-phone'),
)
