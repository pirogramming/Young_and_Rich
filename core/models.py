from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from comp.models import *


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rank = models.IntegerField(default=0)

    gold_list = models.TextField(default="[]")  # list 형식으로

    def append_gold_list(self, x):
        self.gold_list = json.dumps(json.loads(self.gold_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_gold_list(self):
        return json.loads(self.gold_list)

    def count_gold(self):
        gold_list = self.get_gold_list()
        return len(gold_list)

    silver_list = models.TextField(default="[]")

    def append_silver_list(self, x):
        self.silver_list = json.dumps(json.loads(self.silver_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_silver_list(self):
        return json.loads(self.silver_list)

    def count_silver(self):
        silver_list = self.get_silver_list()
        return len(silver_list)

    bronze_list = models.TextField(default="[]")

    def append_bronze_list(self, x):
        self.bronze_list = json.dumps(json.loads(self.bronze_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_bronze_list(self):
        return json.loads(self.bronze_list)

    def count_bronze(self):
        bronze_list = self.get_bronze_list()
        return len(bronze_list)

    badge_list = models.TextField(default="[]")

    def append_badge_list(self, x):
        self.bronze_list = json.dumps(json.loads(self.badge_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_badge_list(self):
        return json.loads(self.badge_list)

    def count_badge(self):
        badge_list = self.get_badge_list()
        return len(badge_list)

    email = models.EmailField(null=True, blank=True, unique=True)

    is_id = models.IntegerField(default=0)  # 0 == id, 1 == co
    star = models.ManyToManyField(Comp, blank=True)
    # Profile1.comp.add(comp1, comp2)
    # for comp in Profile.comp.all()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
