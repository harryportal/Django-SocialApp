import datetime

from django.contrib.contenttypes.models import ContentType
from .models import action
from django.utils import timezone
from datetime import timedelta


def create_action(user, verb, target=None):
    last_minute = timezone.now() - datetime.timedelta(seconds=60)
    # check_for_similar_actions to avoid duplicate entry
    similar_actions = action.objects.filter(user=user, verb=verb, created__gte=last_minute)

    if target and similar_actions:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    # if user has not performed a similar action in the last minute
    if not similar_actions:
        actions = action(user=user, verb=verb, target=target)
        actions.save()
        return True
    return False
