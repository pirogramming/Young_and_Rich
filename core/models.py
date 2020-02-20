import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from comp.models import *
from comp.utils import user_profile_image_path

# Create your models here.
'''
# 정규표현식을 이용한 전화번호 validation
def phone_number_validator(value):
    if not re.match(r'^010[1-9]\d{7}$'):
        raise ValidationError('{}는 올바른 전화번호의 형식이 아닐세!'.format(value))
    '''

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=user_profile_image_path, blank=True)
    total_rank = models.IntegerField(default=0)
    comp = models.ForeignKey(Comp, null=True, blank=True, on_delete=models.CASCADE, related_name='participate_profile')
    comp_rank = models.TextField(default="{}")
    phone_number = models.CharField(max_length=11, blank=True)
    organization = models.CharField(max_length=255, blank=True)

    def append_comp_rank(self, key, value):
        lst = json.loads(self.comp_rank)
        lst[key] = value
        self.comp_rank = json.dumps(lst)
        self.save()

    # 밑에 추가 내장함수는 rank 산정 방식 기획 후 설정

    # gold_list = models.TextField(default="[]")  # list 형식으로
    #
    # def append_gold_list(self, x):
    #     self.gold_list = json.dumps(json.loads(self.gold_list).append(x))
    #     self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.count_badge()
    #
    # def get_gold_list(self):
    #     return json.loads(self.gold_list)
    #
    # def count_gold(self):
    #     gold_list = self.get_gold_list()
    #     return len(gold_list)
    #
    # silver_list = models.TextField(default="[]")
    #
    # def append_silver_list(self, x):
    #     self.silver_list = json.dumps(json.loads(self.silver_list).append(x))
    #     self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.count_badge()
    #
    # def get_silver_list(self):
    #     return json.loads(self.silver_list)
    #
    # def count_silver(self):
    #     silver_list = self.get_silver_list()
    #     return len(silver_list)
    #
    # bronze_list = models.TextField(default="[]")
    #
    # def append_bronze_list(self, x):
    #     self.bronze_list = json.dumps(json.loads(self.bronze_list).append(x))
    #     self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.count_badge()
    #
    # def get_bronze_list(self):
    #     return json.loads(self.bronze_list)
    #
    # def count_bronze(self):
    #     bronze_list = self.get_bronze_list()
    #     return len(bronze_list)
    #
    # badge_list = models.TextField(default="[]")
    #
    # def append_badge_list(self, x):
    #     self.badge_list = json.dumps(json.loads(self.badge_list).append(x))
    #     self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.count_badge()
    #
    # def get_badge_list(self):
    #     return json.loads(self.badge_list)
    #
    # def count_badge(self):
    #     badge_list = self.get_badge_list()
    #     return len(badge_list)

    email = models.EmailField(null=True, blank=True, unique=True)
    star = models.ManyToManyField(Comp, blank=True)


    # Profile1.comp.add(comp1, comp2)
    # for comp in Profile.comp.all()

    def __str__(self):
        return f'{self.user.username} Profile'




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
