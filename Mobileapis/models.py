from django.db import models

class ParcelType(models.Model):
	type = models.CharField(max_length=100,blank=True,null=True)
	

	def __str__(self):
		return str(self.type)

