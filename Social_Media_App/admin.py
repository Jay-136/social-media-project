from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_filter = ["user","posted_at"]
    list_display = ["tag","title","content","posted_at","view_image"]
    search_fields = ["title"]
    
    # exclude = ["image","posted_at","title"]
    @admin.display(empty_value="???")
    def view_image(self, obj):
        return obj.image
    
    
    
@admin.register(CustomUser)    
class CustomUseradmin(admin.ModelAdmin):
    list_display = ["first_name","last_name","email"]
    actions = ["Give_LoginPermission"]
    date_hierarchy = "date_joined"
    fieldsets = [
        (   
            "User",
            {
                "fields" : [("first_name","last_name")],
            },
        ),
        
        (   
            "User advanced detail",
            {
                # "classes" : ["collapse"],
                "classes": ["wide", "collapse"],
                "fields": [("email","username")],
            },
        ),
    ]
    @admin.action(description="Give login permission")
    def Give_LoginPermission(modeladmin, request, queryset):
        queryset.update(is_staff=True)


# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
# admin.site.register(CustomUser)
