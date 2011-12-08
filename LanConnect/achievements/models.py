from django.db.models import *
from django.contrib.auth.models import User
from django.conf import settings
from sorl.thumbnail import ImageField

class Unlock(Model):
	user = ForeignKey(User)
	acheivement = ForeignKey('Acheivement')
	when = DateTimeField(auto_now_add = True)

class Achievement(Model):
	id = CharField(
		max_length=60,
		help_text='A Unique ID assigned for the achievement in format app_name.acheivement_nick',
		unique=True,
	)
	
	achieved_by = ManyToManyField(
		User,
		through=Unlock,
		related_name='acheivements_unlocked'
	)
	
	name = CharField(
		max_length=256, 
		help_text='The name of the achievement'
	)
	
	description = CharField(
		max_length=1024, 
		blank=True
	)
	
	hidden = BooleanField(
		blank=True, 
		default=False,
		help_text='Is the achievement is hidden until it has been earned by the user.'
	)
	
	hidden_from_others = BooleanField(
		blank=True,
		default=False,
		help_text='If another user has earned an achievement, can you view what this achievement is?'
	)
	
	points = PositiveIntegerField(
		help_text='The number of points that you gain for completing this achievement.'
	)
	
	image = ImageField(
		upload_to=settings.ACHIEVEMENT_IMAGES_DIRECTORY,
		thumbnail={
			'size': (20, 20),
			'options': ('crop',)
		},
		null=True,
		help_text='An image for the achievement.'
	)
