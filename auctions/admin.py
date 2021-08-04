from django.contrib import admin

from .models import User, Listing, Comment, Bid, Category


class ListingAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "body") 

class CommentAdmin(admin.ModelAdmin):
    listing_display = ("author", "listing", "body")    


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
admin.site.register(Category)
