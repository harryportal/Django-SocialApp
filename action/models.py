from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class action(models.Model):
    user = models.ForeignKey('auth.User', related_name='actions', on_delete=models.CASCADE, db_index=True)
    verb = models.CharField(max_length=225) # stores the action performed by the user
    created = models.DateTimeField(auto_now_add=True)

    # model attributes for the target model(optional)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='target_obj',
                                  null=True, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')



    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{user} action : {verb}'

