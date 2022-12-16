from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/", views.categorised_index, name="categorised_index"),
    # path("<slug>/", views.index, name="index"),
]
