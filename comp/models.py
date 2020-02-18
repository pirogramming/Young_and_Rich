import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# 결투장
from django.db.models.signals import post_save
from django.dispatch import receiver

from comp.utils import user_answer_upload_to


class Comp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # comp 업로드 한 기업
    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    profile_thumb = models.ImageField(null=True, blank=True)
    back_thumb = models.ImageField(null=True, blank=True)
    prize = models.IntegerField()
    comp_answer = models.FileField(null=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deadline = models.DateField()

    overview_context = models.TextField(null=True, blank=True)  # overview comp 설명
    timeline = models.TextField(null=True, blank=True)  # 마감기한
    prize_context = models.TextField(null=True, blank=True)  # 상금 설명
    evaluation = models.TextField(null=True, blank=True)  # 평가기준
    data_context = models.TextField(null=True, blank=True)  # data 설명
    not_is_main = models.IntegerField(default=1)  # 0 == main, 1 == in class
    star = models.ManyToManyField(User, null=True, blank=True, related_name='comp_star')

    not_is_main = models.IntegerField(default=1)  # 0 == in class, 1 == main

    def __str__(self):
        return self.title


# 결투장 data file 업로드-----
class Comp_File(models.Model):
    file = models.FileField(null=True)
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE)


# 결투장 community Post
class ComPost(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # post 쓴 개인

    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like=models.ManyToManyField(User, related_name='compost_likes', null=True, blank=True)

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
    like=models.ManyToManyField(User, related_name='comcomment_likes' , null=True, blank=True)


# 결투장 code Post
class CodePost(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # code 업로드 한 개인

    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recommend = models.IntegerField(null=True, blank=True)
    like=models.ManyToManyField(User, related_name='codepost_likes', null=True, blank=True)


# 결투장 code에 comment
class CodeComment(models.Model):
    codepost = models.ForeignKey(CodePost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # code에 comment 단 개인

    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commcomment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)  # 대댓글
    like=models.ManyToManyField(User, related_name='codecomment_likes',  null=True, blank=True)


class Answer(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accuracy = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=user_answer_upload_to, null=True)
