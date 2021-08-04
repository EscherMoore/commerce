from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>/add", views.add_wishlist, name="add_wishlist"),
    path("<int:listing_id>/remove", views.remove_wishlist, name="remove_wishlist"),
    path("<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("watchlist", views.wishlist, name="wishlist"),
    path("<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("closed", views.closed, name="closed"),
    path("categories/", views.categories, name="categories"),
    path("results/<int:category_id>", views.results, name="results"),
    path("<int:listing_id>/wishlist", views.remove_wishlist_from_wishlist_page, name="remove_wishlist_from_wishlist_page")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
