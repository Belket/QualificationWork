from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=100, blank=False, default='')
    position = models.CharField(max_length=100, default="")
    coins = models.IntegerField(default=100)  # points to buy information about elements
    level = models.IntegerField(default=1)
    confirmed_elements = models.IntegerField(default=0)
    activation_salt = models.CharField(max_length=30, default="none")

    def __str__(self):
        return self.user.username

    def increase_confirm_element(self):
        self.confirmed_elements += 1

    def set_level(self):
        level = self.confirmed_elements // 4
        self.level = level if level > 0 else 1
        self.save()

    def add_coins(self):
        additional_coins = self.level * 5
        self.coins = self.coins + additional_coins
        self.confirmed_elements += 1
        self.set_level()
        self.save()

    def set_coins(self, coins):
        self.coins = coins


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
    instance.profile.save()

