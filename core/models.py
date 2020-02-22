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
    image = models.ImageField(default='default.png', upload_to=user_profile_image_path, blank=True)
    total_rank = models.IntegerField(default=0)
    comp = models.ForeignKey(Comp, null=True, blank=True, on_delete=models.CASCADE, related_name='participate_profile')
    comp_rank = models.TextField(default="{}")
    phone_number = models.CharField(max_length=11, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=255, blank=True)

    def append_comp_rank(self, key, value):
        lst = json.loads(self.comp_rank)
        lst[key] = value
        self.comp_rank = json.dumps(lst)
        self.save()

    def get_medal_list(self):
        medal_dict = {'gold': 0, 'silver': 0, 'bronze': 0, 'badge': 0}
        # 해당 프로필 유저의 10%되는 등수 가져오기
        # comp_rank의 key와 id가 같은 Comp의 continue_complete로
        # comp_rank의 value를 나눈 것에 따라 10%, 20%, 40%로 메달 부여
        # 그리고 comp_rank의 길이에 따라 배지 부여
        lst = json.loads(self.comp_rank)
        if bool(lst):
            for key, value in lst:
                k = int(key)
                comp = Comp.objects.filter(id=k)
                part = value / comp.continue_complete
                if part <= 0.1:
                    medal_dict['gold'] += 1
                elif 0.1 < part <= 0.2:
                    medal_dict['silver'] += 1
                elif 0.2 < part <= 0.4:
                    medal_dict['bronze'] += 1
            medal_dict['badge'] = len(lst)
        return medal_dict

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
2