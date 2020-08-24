from django.contrib import admin
from datetime import datetime
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["pub_date", "revision_date", "revision_author"]

    def save_model(self, request, obj, form, change):
        # Set the published date.
        if (obj.pub_date is None):
            obj.pub_date = datetime.now()

        # If there's any change, aka revision, in the post, we need to notify who changed it
        # and when the revision was done.
        elif (change):
            obj.revision_date = datetime.now()
            obj.revision_author = request.user

        super().save_model(request, obj, form, change)