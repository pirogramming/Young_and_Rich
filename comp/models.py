import json

from django.contrib.auth.models import User
from django.db import models


# 결투장
from django.db.models.signals import post_save
from django.dispatch import receiver


class Comp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # comp 업로드 한 기업
    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)

    profile_thumb = models.ImageField(null=True, blank=True)
    back_thumb = models.ImageField(null=True, blank=True)
    prize = models.IntegerField()

    created_at = models.DateField()
    updated_at = models.DateField()
    deadline = models.DateTimeField()

    evaluation = models.TextField(null=True, blank=True)
    overview_context = models.TextField(null=True, blank=True)  # overview comp 설명
    data_context = models.TextField(null=True, blank=True)  # data 설명
    not_is_main = models.IntegerField(default=1)  # 0 == main, 1 == in class
    team_number = models.IntegerField(default=0)  # 참여팀 수


# 결투장 data file 업로드
class FileUp(models.Model):
    file = models.FileField()
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE)  # data 올리는 comp
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # data 올리는 기업


# 결투장 community Post
class ComPost(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # post 쓴 개인

    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 결투장 community Comment
class ComComment(models.Model):
    com_post = models.ForeignKey(ComPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # comment 쓴 개인

    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ComCommComment(models.Model):
    comment = models.ForeignKey(ComComment, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 결투장 code Post
class CodePost(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # code 업로드 한 개인

    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    recommend = models.IntegerField(null=True, blank=True)


# 결투장 code에 comment
class CodeComment(models.Model):
    code_post = models.ForeignKey(CodePost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # code에 comment 단 개인

    context = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Answer(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE)
    accuracy = models.FloatField()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    rank = models.IntegerField(default=0)

    # gold
    gold_list = models.TextField(default="[]")  # list 형식으로

    def append_gold_list(self, x):
        self.gold_list = json.dumps(json.loads(self.gold_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_gold_list(self):
        return json.loads(self.gold_list)

    def count_gold(self):
        gold_list = self.get_gold_list()
        return len(gold_list)

    # silver
    silver_list = models.TextField(default="[]")

    def append_silver_list(self, x):
        self.silver_list = json.dumps(json.loads(self.silver_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_silver_list(self):
        return json.loads(self.silver_list)

    def count_silver(self):
        silver_list = self.get_silver_list()
        return len(silver_list)

    # bronze
    bronze_list = models.TextField(default="[]")

    def append_bronze_list(self, x):
        self.bronze_list = json.dumps(json.loads(self.bronze_list).append(x))
        self.rank = self.count_gold() * 10 + self.count_silver() * 5 + self.count_bronze() * 3 + self.badge

    def get_bronze_list(self):
        return json.loads(self.bronze_list)

    def count_bronze(self):
        bronze_list = self.get_bronze_list()
        return len(bronze_list)

    # badge
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
    comp = models.ManyToManyField(Comp)
    # Profile1.comp.add(comp1, comp2)
    # for comp in Profile.comp.all()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()