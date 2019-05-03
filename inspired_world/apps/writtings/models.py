from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from inspired_world.apps.authentication.models import User
from inspired_world.apps.profiles.models import Profile
from inspired_world.apps.core.models import TimestampModel


class Writting(TimestampModel):

    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        'writtings.Tag', related_name='writtings'
    )

    def __str__(self):
        return self.title


class Tag(TimestampModel):
    """This class defines the tag model"""

    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return '{}'.format(self.tag)


def pre_save_writting_receiver(sender, instance, *args, **kwargs):
    """
    Method uses a signal to add slug to an article before saving it
    A slug will always be unique
    """
    if instance.slug:
        return instance
    slug = slugify(instance.title)
    num = 1
    unique_slug = slug
    # loops until a unique slug is generated
    while Writting.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%s" % (slug, num)
        num += 1

    instance.slug = unique_slug


# Called just before a save is made in the db
pre_save.connect(pre_save_writting_receiver, sender=Writting)
