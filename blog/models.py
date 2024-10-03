# blog/models.py
# Define the data obects for our application
from django.db import models



# When do you need to use the makemigration command!!!!! QUIZ

# Create your models here.
class Article(models.Model):
    '''
    Encapsulates the idea of one Article by some author
    '''
    # data attributes of an Article
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
