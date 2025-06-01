from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.db.models import Max

# Create your models here.
class DATT(models.Model):
    secure = models.IntegerField(default=0)
    addr = models.IntegerField()
    room = models.IntegerField()
    CO = models.CharField(max_length=8)
    HUM = models.CharField(max_length=8)
    TEMP = models.CharField(max_length=8)
    time = models.TimeField(auto_now=True)

@receiver(post_save, sender=DATT)
def clean_old_records(sender, instance, created, **kwargs):
    if created:
        # Получаем 11-ю запись по времени (если существует)
        to_delete = DATT.objects.filter(
            addr=instance.addr,
            room=instance.room
        ).order_by('-id').values_list('id', flat=True)[10:]
        
        if to_delete.exists():
            with transaction.atomic():
                DATT.objects.filter(id__in=list(to_delete)).delete()
