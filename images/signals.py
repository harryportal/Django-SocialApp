from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import Image

@receiver(m2m_changed, sender=Image.users_liked.through)
def update_image_like_count(sender, instance, **kwargs):
    instance.total_likes = instance.users_liked.count()
    instance.save()
