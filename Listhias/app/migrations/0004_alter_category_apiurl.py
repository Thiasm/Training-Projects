# Generated by Django 5.1.4 on 2025-01-07 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='apiUrl',
            field=models.URLField(choices=[('movie', 'https://api.themoviedb.org/3/search/movie'), ('tv_show', 'https://api.themoviedb.org/3/search/tv'), ('anime', 'http://animedb.me/api/shows/title'), ('book', 'https://api2.isbndb.com/books/'), ('manga', 'https://api.mangadex.org/manga'), ('music', 'https://musicbrainz.org/ws/2/'), ('video_game', 'https://api.igdb.com/v4/games'), ('todo_list', 'NOT NEEDED')]),
        ),
    ]
