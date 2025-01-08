from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):

    class CategoryTypes(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')
        ANIME = 'anime', _('Anime')
        BOOK = 'book', _('Book')
        MANGA = 'manga', _('Manga')
        MUSIC = 'music', _('Music')
        VIDEO_GAME = 'video_game', _('Video Game')
        TODO_LIST = 'todo_list', _('Todo List')

    CATEGORY_URLS = {
        CategoryTypes.MOVIE: 'https://api.themoviedb.org/3/search/movie',
        CategoryTypes.TV_SHOW: 'https://api.themoviedb.org/3/search/tv',
        CategoryTypes.ANIME: 'http://animedb.me/api/shows/title',
        CategoryTypes.BOOK: 'https://api2.isbndb.com/books/',
        CategoryTypes.MANGA: 'manga',
        CategoryTypes.MUSIC: 'https://musicbrainz.org/ws/2/',
        CategoryTypes.VIDEO_GAME: 'video_game',
        CategoryTypes.TODO_LIST: 'NOT NEEDED',
    }

    title = models.CharField(max_length = 25)
    type = models.CharField(max_length = 10, choices = CategoryTypes.choices)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
        
    def get_api_url(self):
        return self.CATEGORY_URLS[self.type]
    
    def item_count(self):
        return self.items.count()
    
class Item(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField(blank = True)
    complete = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    image = models.URLField(max_length = 200, blank = True)
    category = models.ForeignKey(Category, related_name = "items", on_delete = models.CASCADE)

    def __str__(self):
        return self.title
