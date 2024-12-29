from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    
    class CategoryUrlTypes(models.TextChoices):
        MOVIE = 'https://api.themoviedb.org/3/search/movie',
        TV_SHOW = 'https://api.themoviedb.org/3/search/tv' 
        ANIME = 'http://animedb.me/api/shows/title', #anidb
        BOOK = 'https://api2.isbndb.com/books/', #goodreads
        MANGA = 'manga', #anisearch
        MUSIC = 'https://musicbrainz.org/ws/2/', #apple music
        VIDEO_GAME = 'video_game', #imdb
        TODO_LIST = 'NOT NEEDED',

    class CategoryTypes(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')
        ANIME = 'anime', _('Anime')
        BOOK = 'book', _('Book')
        MANGA = 'manga', _('Manga')
        MUSIC = 'music', _('Music')
        VIDEO_GAME = 'video_game', _('Video Game')
        TODO_LIST = 'todo_list', _('Todo List')

    title = models.CharField(max_length=25)
    type = models.CharField(max_length=10, choices = CategoryTypes.choices)
    apiUrl = models.URLField(max_length=200, choices = CategoryUrlTypes.choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def getApiUrl(self):
        return self.CategoryUrlTypes[self.type].value

class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    image = models.URLField(max_length=200, blank=True)
    # category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
        # return reverse('item_detail', kwargs={'pk': self.pk})    

# Add Category -> Create new Category Object
# Add Item -> Create new Item Object -> Link it to the related Category
# How to access related category inside of it ?
# - By name (from URL or whatever) ?
# - Create an Item_List Object ?