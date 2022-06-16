from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='users/%y/%m/%d', blank=True)

    def __str__(self):
        return f'Username: {self.user.username} '


# an extra model for linking the user followers and following attribute
class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-date_created',)


    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# a method to add the following attribute to django auth model
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers',
                                                            symmetrical=False))


