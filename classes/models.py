from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
	prefixed_id = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # no cascade, class will be left unmanaged

	def __str__(self):
		return self.prefixed_id + ' ' + self.name

class Enrollment(models.Model):
	course_id = models.ForeignKey(Class, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)