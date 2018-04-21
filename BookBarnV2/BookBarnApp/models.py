from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from datetime import datetime, time, date, timedelta
from django.contrib.auth.models import User

#default values of null and blank is False

class Authors(models.Model):
    aid = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(10)], verbose_name="Author's ID", help_text="Use 'A' as prefix in 10 character Author's ID")
    fName = models.CharField(max_length=50, null=True, blank=False, verbose_name="First Name")
    lName = models.CharField(max_length=50, blank=True, null=True, verbose_name="Last Name")
    about = models.TextField(blank=True, null=True, verbose_name="About the Author", help_text="Add description about the Author")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = 'authors'
        ordering = ['fName', 'lName']
    
    def __str__(self):
        if (self.lName != ''):
            return '%s : %s' % (self.aid, self.fName + ' ' + self.lName)
        else:
             return '%s : %s' % (self.aid, self.fName)

    def get_full_name(self):
        return self.fName + ' ' + self.lName


class Genres(models.Model):
    gid = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(10)], verbose_name="Genre's ID", help_text="Use 'G' as prefix in 10 character Genre's ID")
    gName = models.CharField(max_length=255, null=True, blank=False, verbose_name="Genre")

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        db_table = 'genres'
        ordering = ['gName',]

    def __str__(self):
        return '%s : %s' % (self.gid, self.gName)

    def get_absolute_url(self):
        return "/category/{gid}/".format(gid=self.gid)


class Publishers(models.Model):
    pid = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(10)], verbose_name="Publisher's ID", help_text="Use 'P' as prefix in 10 character Publisher's ID")
    pName = models.CharField(max_length=255, null=True, blank=False, verbose_name="Publisher")

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        db_table = 'publishers'
        ordering = ['pName',]

    def __str__(self):
        return '%s : %s' % (self.pid, self.pName)


class Books(models.Model):
    isbn = models.CharField(primary_key=True, validators=[MinLengthValidator(10)], max_length=10, verbose_name="ISBN", help_text="ISBN (or ISBN 10): 10 digit value")
    bookTitle = models.CharField(max_length=255, null=True, blank=False, verbose_name="Title of Book")
    description = models.TextField(blank=True, null=True, verbose_name="Description", help_text="Enter the book description")
    pageCount = models.PositiveIntegerField(null=False, blank=False, default = 0, verbose_name="Number of Pages")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0.00), MaxValueValidator(5.00)], verbose_name="Rating", help_text="Rating should be in between 0.0 and 5.0")
    language = models.CharField(max_length=20, blank=True, null=True, verbose_name="Language")
    coverImage = models.URLField(max_length=255, blank=True, null=True, verbose_name="Cover Image URL", help_text="Enter image URL")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)], verbose_name="Price") 
    publishedDate = models.DateField(blank=True, null=True, verbose_name="Publishing Date")
    publisher = models.ForeignKey(Publishers, on_delete=models.PROTECT, related_name='books', verbose_name="Publisher")
    # voteCount = models.PositiveIntegerField(default=0, verbose_name="Number of Votes")
    authors = models.ManyToManyField(Authors, related_name='books', db_table='books_authors', verbose_name="Authors")
    genres = models.ManyToManyField(Genres, related_name='books', db_table='books_genres', verbose_name="Genres")
    booksCount = models.PositiveIntegerField(null=False, blank=False, default = 0, verbose_name="Number of Books")
    bookFormat = models.CharField(max_length=20, blank=True, null=True, verbose_name="Book Format", help_text="eg. Paperback, Hardcover")

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = 'books'
        ordering = ['bookTitle',]

    def __str__(self):
        return '%s : %s' % (self.isbn, self.bookTitle)

    def get_absolute_url(self):
        return "/book/{isbn}/".format(isbn=self.isbn)



# First name, last name, email, password already in User model

class UserProfiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    phoneNumber = models.CharField(max_length=10, validators=[MinLengthValidator(10, message=' '), RegexValidator(r'\d+', message="Enter a valid 10 digit Phone No.")], null=True, blank=False, verbose_name="Phone No.")
    address1 = models.CharField(max_length=255, null=True, blank=False, verbose_name="Address Line 1")
    address2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=255, null=True, blank=False, verbose_name="City")
    state = models.CharField(max_length=255, null=True, blank=False, verbose_name="State")
    pinCode = models.CharField(max_length=6, validators=[MinLengthValidator(6, message=' '), RegexValidator(r'\d+', message="Enter a valid 6 digit PIN Code")], null=True, blank=False, verbose_name="PIN Code")

    class Meta:
        db_table = "userprofiles"
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name 
    get_full_name.short_description = "Full Name"

    def get_username(self):
        return self.user.username
    get_username.short_description = "Username"

    def get_email(self):
        return self.user.email
    get_email.short_description = "E-mail"

    def get_full_address(self):
        return self.address1 + ', ' + self.address2 + '\n' + self.city + '\n' + self.state + ' - ' + self.pinCode
    get_full_address.short_description = "Address"

    def get_last_login(self):
        return self.user.last_login
    get_last_login.short_description = "Last Login"

    def get_date_joined(self):
        return self.user.date_joined
    get_date_joined.short_description = "Date Joined"

    def get_is_active(self):
        return self.user.is_active
    get_is_active.short_description = "Active"

    def get_is_staff(self):
        return self.user.is_staff
    get_is_staff.short_description = "Staff"

    def get_is_superuser(self):
        return self.user.is_superuser
    get_is_superuser.short_description = "Super User"