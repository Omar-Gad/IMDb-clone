# Generated by Django 4.0.3 on 2022-04-03 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watchlist_app', '0002_review_streamplatform_watchlist_delete_movie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='watchlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='watchlist_app.watchlist'),
        ),
    ]
