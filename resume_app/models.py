from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100, default="Anandhu TS")
    title = models.CharField(max_length=200, default="Python Developer")
    email = models.EmailField(default="anandhutsarun@gmail.com")
    phone = models.CharField(max_length=15, default="+918281350626")
    linkedin = models.URLField(default="https://linkedin.com/in/anandhu-ts-bba348278")
    location = models.CharField(max_length=100, default="Kollam, Kerala")
    summary = models.TextField(default="Passionate and self-motivated Python Developer with a strong foundation in programming, problem-solving, and web development. Eager to leverage technical skills in Python, Django, and database management to develop innovative software solutions. Enthusiastic about learning new technologies and contributing to dynamic and growth-oriented teams.")
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)  # New field for photo

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.CharField(max_length=100)  # e.g., Programming Languages
    name = models.CharField(max_length=100)      # e.g., Python

    def __str__(self):
        return f"{self.category}: {self.name}"

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    cgpa = models.FloatField()

    def __str__(self):
        return self.degree

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Training(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name