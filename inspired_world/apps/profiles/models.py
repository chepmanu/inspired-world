from django.conf import settings
from django.db import models

# User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    """This class represents the user profile model."""

    # resticting user to have one and only one profile
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.TextField(blank=True)
    interests = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(
        'writtings.Writting', symmetrical=False,
        related_name='users_fav_writtings')
    follows = models.ManyToManyField(
        'self',
        related_name='follower',
        symmetrical=False
    )

    def __str__(self):
        return '{}'.format(self.user.email)

    def favorite(self, writting):
        self.favorites.add(writting)

    def unfavorite(self, writting):
        self.favorites.remove(writting)

    def follow(self, profile):
        """Follow another user if not already following"""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow another user if followed"""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if a user is followed \
        by active user. False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_follower(self, profile):
        """Returns True if a user is following active user; False otherwise."""
        return self.follower.filter(pk=profile.pk).exists()
