from django.contrib import admin
from .models import *
from .forms import SocialAdminForm
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.

@admin.register(Post)
class Postadmin(ImportExportActionModelAdmin):
    list_filter = ["user","posted_at"]
    list_display = ["tag","title","content","posted_at","view_image","user"]
    search_fields = ["title"]
    search_help_text = "Searching based on title"
    form = SocialAdminForm
    # list_display_links = ["title"]
    list_select_related = ["user"]
    list_per_page = 4
    save_as = True
    save_as_continue = False
    ordering = ["-title"]
    
    # exclude = ["image","posted_at","title"]
    @admin.display(empty_value="???")
    def view_image(self, obj):
        return obj.image
    
class PostInline(admin.TabularInline):
    model = Post
    fields = ['title',
            'image',
            'tag',
            'user',
            'posted_at',
            'updated_at']
    readonly_fields = ['posted_at','updated_at']
    
@admin.register(CustomUser)    
class CustomUseradmin(ImportExportActionModelAdmin):
    list_display = ["id","username","display_fullname","email"]
    list_display_links = ["username"]
    actions = ["Give_LoginPermission"]
    date_hierarchy = "date_joined"
    inlines = [PostInline]
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

    def display_fullname(self,obj):
        return f"{obj.first_name} {obj.last_name}"
    
    display_fullname.short_description = "Full Name"

# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
# admin.site.register(CustomUser)
