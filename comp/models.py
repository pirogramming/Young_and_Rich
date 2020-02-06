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
    accuracy = models.FloatField()g
