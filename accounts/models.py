
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    is_verified = models.BooleanField(
        default=False,
        help_text="Check to grant this user a verified badge on all their listings"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Seller profile picture"
    )

    def __str__(self):
        return f"{self.user.username} Profile"


# Automatically create a profile when a new user registers
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


# Automatically save the profile when the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
