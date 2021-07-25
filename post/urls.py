from django.urls import path
from .views import index, about, post, contact, search, view_all, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
	path("", index, name="home"),
	path("about/", about, name="about"),
	path("contact/", contact, name="contact"),
	path("search/", search, name="search"),
	path("View_All/<str:query>/", view_all, name="view_all"),
	path("post/<int:id>/<slug:slug>/", post, name="post"),
	path("add_post/", PostCreateView.as_view(), name="add-post"),
	path("post/update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
	path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
]
