from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
rate_list = [1, 2, 3, 4, 5]


class Profile(models.Model):
	"""
	Model for profile.
	Attributes:
		user
	"""
	user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
	fullname = models.CharField(max_length=40, blank=True, null=True)
	address = models.CharField(max_length=40, blank=True, null=True)
	status = models.TextField(max_length=100, blank=True, null=True)
	editor = models.BooleanField(default=False)
	bio = models.TextField(blank=True, null=True)
	image = models.ImageField(default="default.png", upload_to="profile_pics")
	rate = models.FloatField(default=0)

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		"""
		Overrides the same method.
		To reduce the size of the image.
		:return:
		"""
		super().save()
		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
