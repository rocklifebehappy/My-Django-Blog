from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post, Subscribers, Contact, Comment, SubComment
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User


# Create your views here.

def index(request):
	if request.method == "GET":
		email = request.GET.get('email')
		if email:
			Subscribers(email=email).save()
	week_ago = datetime.date.today() - datetime.timedelta(days=7)
	trends = Post.objects.filter(time_upload__gte=week_ago).order_by("-read")
	top_authors = User.objects.filter(profile__rate=0.0)
	print(top_authors)
	authors_posts = [Post.objects.filter(auther=auther).first() for auther in top_authors]
	all_posts = Paginator(Post.objects.filter(publish=True), 3)
	page = request.GET.get('page')
	try:
		posts = all_posts.page(page)
	except PageNotAnInteger:
		posts = all_posts.page(1)
	except EmptyPage:
		posts = all_posts.page(all_posts.num_pages)
	context = {
		'posts': posts,
		'trends': trends,
		'author_post': authors_posts,
		'pop_post': Post.objects.order_by('-read')
	}
	return render(request, "index.html", context)


def about(request):
	return render(request, "about.html", context={})


def post(request, id, slug):
	try:
		post = Post.objects.get(pk=id, slug=slug)
		if request.method == "POST":
			comm = request.POST.get("comm")
			comm_id = request.POST.get("comm_id")
			if comm_id:
				SubComment(post=post, user=request.user, comm=comm, comment=Comment.objects.get(id=comm_id)).save()
			else:
				Comment(post=post, user=request.user, comment=comm).save()
		comments = []
		for c in Comment.objects.filter(post=post):
			comments.append([c, SubComment.objects.filter(comment=c)])
		context = {
			'post': post,
			'comments': comments,
			'pop_post': Post.objects.order_by("-read")[:9]
		}
	except:
		raise Http404("Post doesn't exist.")
	post.read += 1
	post.save()
	return render(request, "blog-single.html", context)


def contact(request):
	if request.method == "POST":
		name = f'{request.POST.get("fname")} {request.GET.get("lname")}'
		email = request.POST.get("email")
		mobile = request.POST.get("mobile")
		message = request.POST.get("message")
		Contact(name=name, email=email, mobile=mobile, message=message).save()
	return render(request, "contact.html", context={})


def search(request):
	q = request.GET.get('q')
	posts = Post.objects.filter(
		Q(title__icontains=q) | Q(overview__icontains=q) | Q(auther__username__icontains=q) |
		Q(categories__title__icontains=q)
	).distinct().order_by("-id")
	context = {
		'posts': posts,
		'title': f'Search Results for {q}',
		'pop_post': Post.objects.order_by('-read')[:9]
	}
	return render(request, "all.html", context)


def view_all(request, query):
	acpt = ['trending', 'popular']
	q = query.lower()
	if q in acpt:
		if q == acpt[0]:
			week_ago = datetime.date.today() - datetime.timedelta(days=7)
			context = {
				'posts': Post.objects.filter(time_upload__gte=week_ago).order_by("-read"),
				'title': "Trending Posts",
				'pop_post': Post.objects.order_by("-read")[:9],
			}
		elif q == acpt[1]:
			context = {
				'posts': Post.objects.order_by("-read"),
				'title': "Trending Posts",
				'pop_post': Post.objects.order_by("-read")[:9],
			}
		else:
			pass
	return render(request, "all.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
	"""
	It gives the post create.
	It inherits the LoginRequiredMixin to ensure the login is done.
	"""
	model = Post
	template_name = "post_form.html"
	fields = ["title", "overview", "body_text", "thumbnail", "publish", "categories"]

	def form_valid(self, form):
		form.instance.auther = self.request.user
		return super().form_valid(form)

	def get_success_url(self, *args, **kwargs):
		return reverse("post", kwargs={'id': self.object.id, 'slug': self.object.slug})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	template_name = "post_form.html"
	fields = ["title", "overview", "body_text", "thumbnail", "publish", "categories"]

	def form_valid(self, form):
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user.username == post.auther.username:
			return True
		else:
			return False

	def get_success_url(self, *args, **kwargs):
		return reverse("post", kwargs={'id': self.object.id, 'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	"""
	To delete the post.
	It inherits LoginRequiredMixin, UserPassesTestMixin to ensure the login and proper authentication.
	"""
	model = Post
	template_name = "post_confirm_delete.html"

	def test_func(self):
		"""
		This is the test to ensure if the user has the proper authentication to delete the post.
		Author of the post and the user must be same to delete the post.
		:return: True if author and user are same else False(that gives 403 error).
		"""
		post = self.get_object()
		if self.request.user.username == post.auther.username:
			return True
		else:
			return False

	def get_success_url(self, *args, **kwargs):
		return reverse("profile", kwargs={})
