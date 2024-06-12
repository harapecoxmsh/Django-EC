
from django.urls import path
from .views import signupfunc, signinfunc, logoutfunc, listfunc, ItemCreate, detailfunc, ItemSearch, like_item, liked_items_list, item_filter


urlpatterns = [
    path("signup/", signupfunc, name="signup"),
    path("signin/", signinfunc, name="signin"),
    path("logout/", logoutfunc, name='logout'),
    path("list/", listfunc, name="list"),
    path("create/", ItemCreate.as_view(), name="create"),
    path("detail/<int:pk>", detailfunc, name="detail"),
    path("search_item/", ItemSearch.as_view(), name="search_item"),
    path("like/<int:pk>", like_item, name="like_item"),
    path("myliked/", liked_items_list, name="liked_items_list"),
    path("filter_item/", item_filter, name="filter_item")


]
