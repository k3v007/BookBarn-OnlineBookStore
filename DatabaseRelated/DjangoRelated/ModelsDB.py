from django.db import models

#default values of null and blank is False

class Authors(models.Model):
    aid = models.CharField(primary_key=True, max_length=10)
    fName = models.CharField(max_length=50)
    lName = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = 'authors'
    
    def __str__(self):
        return '%s : %s' % (self.aid, self.fName + self.lName)


class Genres(models.Model):
    gid = models.CharField(primary_key=True, max_length=10)
    gName = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        db_table = 'genres'

    def __str__(self):
        return '%s : %s' % (self.gid, self.gName)


class Publishers(models.Model):
    pid = models.CharField(primary_key=True, max_length=10)
    pName = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        db_table = 'publishers'

    def __str__(self):
        return '%s : %s' % (self.pid, self.pName)


class Books(models.Model):
    isbn = models.CharField(primary_key=True, max_length=10)
    bookTitle = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    pageCount = models.IntegerField(null=False, blank=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    coverImage = models.URLField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publishedDate = models.DateField(blank=True, null=True)
    publisher_pid = models.ForeignKey(Publishers, on_delete=models.CASCADE)
    voteCount = models.IntegerField(blank=True, null=True)
    authors = models.ManyToManyField(Authors, related_name='books', db_table='books_publishers')
    genres = models.ManyToManyField(Genres, related_name='books', db_table='books_genres')

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = 'books'

    def __str__(self):
        return '%s : %s' % (self.isbn, self.bookTitle)
