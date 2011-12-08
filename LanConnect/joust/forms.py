#django framework
from django.forms.forms import Form
from django.forms import ModelForm
from django.forms.fields import *
from django.forms.fields import SelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.conf import settings
from gettext import gettext as _
#apps
#from merlin.wizards.session import SessionWizard
#joust
from models import Event, Tournament
from signals import signup_extras_add, signup_extras_process

class TioImportForm(Form):
	file = FileField()
	
class UserSignupForm(Form):
	#def __init__(self, *args, **kwargs):
	#	signup_extras_add.send(sender=self)
	#	super(UserSignupForm, self).__init__(*args, **kwargs)
	
	handle = CharField(required=True, help_text=_(u"The name or nickname you wish to be identified by.  This must be unique.  This is also used to allow you to log in to the system."))
	email = EmailField(required=True, help_text=_(u"Email Address is used to claim your account if desired."))
	first_name = CharField(required=False)
	last_name = CharField(required=False)
	
	if settings.JOUST_SMS_NOTIFICATIONS == True:
		mobile_number = CharField(
			required=False, 
			max_length=25,
			help_text = _(u"Used to notify you by SMS of your upcoming matches")
		)

class UserTournamentForm(Form):
	def __init__(self, *args):
		super(UserTournamentForm,self).__init__(*args)
		tournament_list = Event.objects.get(in_progress=True).tournaments_run.all()
		choices = [( t.pk, t ) for t in tournament_list]
		
		#choices[0].extend(Event.objects.get(in_progress=True).tournaments_run.all())
		self.fields['tournaments'].widget = FilteredSelectMultiple(verbose_name="Tournaments", is_stacked=False, choices=choices)
		self.fields['tournaments'].choices = choices
	#Need to make a list of tournaments we can sign up to .......
	tournaments = MultipleChoiceField(required=True)

class CreateTournamentForm(ModelForm):
	class Meta:
		model = Tournament
		exclude = ('entrants', 'finished_at', 'event')

class BracketGenerationForm(Form):
	class Meta:
		model = Tournament
        
class EditTournamentForm(ModelForm):
    class Meta:
        #I know this is likely wrong, at least for now since we are editing. 
        #Perhaps, the best soloution is to just use the CreateTournament form, and just in the view route the data based on wether
        #the tournament exists or not?
        model = Tournament
        exclude = ( 'entrants', 'finished_at', 'event')
        
class ModifySignupForm(Form):
    #This should be able to modify a participants assigned tournaments.
    #Its not for editing users.
    #It *could* use a similar form as the UserTournamentForm (or even extend it)
    def __init__(self, *args):
        super(ModifySignupForm, self).__init__(*args)

class ManageUserForm(Form):
    #This is a precursor to our former form. It should allow us to pick from a list of users, the one we want to 
    #manage.
    #
    #This covers both manual signups and managing of the users signups. 
    def __init__(self, *args):
        super(ManageUserForm, self).__init__(*args)       
