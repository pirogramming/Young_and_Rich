import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# 결투장
from django.db.models.signals import post_save
from django.dispatch import receiver




class Comp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # comp 업로드 한 기업
    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    profile_thumb = models.ImageField(null=True, blank=True)
    back_thumb = models.ImageField(null=True, blank=True)
    prize = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deadline = models.DateTimeField()

    evaluation = models.TextField(null=True, blank=True)
    overview_context = models.TextField(null=True, blank=True)  # overview comp 설명
    data_context = models.TextField(null=True, blank=True)  # data 설명
    not_is_main = models.IntegerField(default=1)  # 0 == main, 1 == in class
    team_number = models.IntegerField(default=0)  # 참여팀 수

    def __str__(self):
        return self.title


# 결투장 data file 업로드-----
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

    def __str__(self):
        return self.title


# 결투장 community Comment
class ComComment(models.Model):
    compost = models.ForeignKey(ComPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # comment 쓴 개인

    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    commcomment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)  # 대댓글


# 결투장 code Post
class CodePost(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # code 업로드 한 개인

    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recommend = models.IntegerField(null=True, blank=True)


# 결투장 code에 comment
class CodeComment(models.Model):
    code_post = models.ForeignKey(CodePost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # code에 comment 단 개인

    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name='answer')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    accuracy = models.FloatField(null=True, blank=True)
    rank = models.IntegerField( null=True, blank=True)

    file = models.FileField()


