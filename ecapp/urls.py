
from django.urls import path
from .views import signupfunc, signinfunc, logoutfunc, listfunc, ItemCreate, detailfunc, goodfunc, ItemSearch


urlpatterns = [
    path("signup/", signupfunc, name="signup"),
    path("signin/", signinfunc, name="signin"),
    path("logout/", logoutfunc, name='logout'),
    path("list/", listfunc, name="list"),
    path("create/", ItemCreate.as_view(), name="create"),
    path("detail/<int:pk>", detailfunc, name="detail"),
    path("good/<int:pk>", goodfunc, name="good"),
    path("search_item/", ItemSearch.as_view(), name="search_item"),

]
