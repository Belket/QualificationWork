from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=100, blank=False)
    coins = models.IntegerField(default=100)  # points to buy information about elements

    def __str__(self):
        return self.user.username

    def add_coins(self, additional_coins):
        self.coins = self.coins + additional_coins
        self.save()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
    instance.profile.save()

