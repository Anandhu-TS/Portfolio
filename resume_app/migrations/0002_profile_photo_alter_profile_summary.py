# Generated by Django 5.0.6 on 2025-03-07 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='summary',
            field=models.TextField(default='Passionate and self-motivated Python Developer with a strong foundation in programming, problem-solving, and web development. Eager to leverage technical skills in Python, Django, and database management to develop innovative software solutions. Enthusiastic about learning new technologies and contributing to dynamic and growth-oriented teams.'),
        ),
    ]
