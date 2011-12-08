
from django.dispatch import Signal

signup_extras_add = Signal(providing_args=[])
signup_extras_process = Signal(providing_args=['user'])