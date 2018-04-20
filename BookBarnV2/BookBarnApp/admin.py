from django.contrib import admin
from BookBarnApp.models import Books, Authors, Genres, Publishers, UserProfiles

# Register your models here.
admin.site.site_header = 'BookBarn Admin'

class BooksAdmin(admin.ModelAdmin):
    list_display = ['isbn', 'bookTitle', 'pageCount', 'price', 'publishedDate', 'rating', 'booksCount', 'bookFormat']
    list_display_links = ['bookTitle',]
    # list_filter = ['publishedDate', ['authors', admin.RelatedOnlyFieldListFilter]]
    date_hierarchy = 'publishedDate'
    search_fields = ['bookTitle', 'isbn',]
    raw_id_fields = ["publisher",]
    filter_horizontal = ['authors', 'genres',]
    

class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['aid', 'fName', 'lName', 'about',]
    search_fields = ['fName', 'lName', 'aid',]


class GenresAdmin(admin.ModelAdmin):
    list_display = ['gid', 'gName',]
    list_display_links = ['gName',]
    search_fields = ['gName', 'gid',]


class PublishersAdmin(admin.ModelAdmin):
    list_display = ['pid', 'pName',]
    list_display_links = ['pName',]
    search_fields = ['pName', 'pid',]


class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_username', 'get_email', 'phoneNumber', 'get_is_active', 'get_is_staff', 'get_is_superuser', 'get_last_login', 'get_date_joined']
    raw_id_fields = ['user']

admin.site.register(Books, BooksAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Publishers)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(UserProfiles, UserProfilesAdmin)