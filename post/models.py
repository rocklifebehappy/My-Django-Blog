from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from django.utils.text import slugify


class Subscribers(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email


class Categories(models.Model):
	title = models.CharField(max_length=20)

	def __str__(self):
		return self.title


class Post(models.Model):
	title = models.CharField(max_length=50)
	overview = models.TextField()
	body_text = RichTextUploadingField(null=True)
	slug = models.TextField(null=True, blank=True)
	time_upload = models.DateTimeField(auto_now_add=True)
	auther = models.ForeignKey(User, on_delete=models.CASCADE)
	thumbnail = models.ImageField(upload_to="Thumbnails")
	publish = models.BooleanField()
	categories = models.ManyToManyField(Categories)
	read = models.IntegerField(default=0)

	class Meta:
		ordering = ["-pk"]

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)


class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	mobile = models.CharField(max_length=12)
	message = models.TextField()
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comment = models.TextField()

	def __str__(self):
		return self.post.title


class SubComment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

	def __str__(self):
		return self.comment.comment


class Rate(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
	rate = models.IntegerField()
	rater = models.ForeignKey(User, related_name="rater", on_delete=models.CASCADE)

	def __str__(self):
		return self.post.title
