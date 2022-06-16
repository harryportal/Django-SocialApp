from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True) # optional
    url = models.URLField()
    image = models.ImageField(upload_to='images/%y/&m/%d')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True, db_index=True)
    total_likes = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return f'Title: {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug: # generate a slug incase it isn't given
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


#image_by_popularity = Image.objects.annotate(total_likes=models.Count('users_liked')).order_by('-total_likes')