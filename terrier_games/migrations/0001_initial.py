# Generated by Django 4.2.16 on 2024-11-22 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('release_year', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('genre', models.CharField(choices=[('strategy', 'Strategy'), ('family', 'Family'), ('party', 'Party'), ('other', 'Other')], max_length=20)),
                ('stock_quantity', models.IntegerField()),
                ('image_url', models.URLField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('cart', 'Cart'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrier_games.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('comment_date', models.DateField(auto_now_add=True)),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('board_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrier_games.boardgame')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrier_games.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('board_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrier_games.boardgame')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrier_games.order')),
            ],
        ),
    ]
