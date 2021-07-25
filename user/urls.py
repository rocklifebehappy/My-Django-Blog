from django.urls import path
from .views import register, edit_profile, profile, others_profile

urlpatterns = [
    path("", register, name="register"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("profile/", profile, name="profile"),
    path("others-profile/<str:user>/", others_profile, name="other_profile")
]
