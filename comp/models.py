import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from datetime import date

# 결투장
from django.db.models.signals import post_save
from django.dispatch import receiver

from comp.utils import user_answer_upload_to, comp_answer_upload_to


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo_thumb = models.ImageField()
    address = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email', max_length=255)
    phone = models.CharField(max_length=225)


class Comp(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # comp 업로드 한 기업
    title = models.CharField(max_length=255)
    context = models.TextField()
    profile_thumb = models.ImageField(null=True, blank=True)
    back_thumb = models.ImageField(null=True, blank=True)
    prize = models.IntegerField()
    comp_answer = models.FileField(blank=True, upload_to=comp_answer_upload_to)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deadline = models.DateField()

    overview_context = models.TextField()  # overview comp 설명
    timeline = models.TextField()  # 마감기한
    prize_context = models.TextField()  # 상금 설명
    evaluation = models.TextField()  # 평가기준
    data_context = models.TextField()  # data 설명
    not_is_main = models.IntegerField(default=1)  # 0 == main, 1 == in class
    star = models.ManyToManyField(User,  blank=True, related_name='comp_star')

    choice_list = ((0, 0), (1, 1))

    not_is_main = models.IntegerField(default=1, choices=choice_list)  # 0 == in class, 1 == main
    continue_complete = models.IntegerField(default=0, choices=choice_list)  # 0 == 대회 진행 중, 1 == 대회 완료

    def is_star(self, request):
        if self.star.filter(id=request.user.id).exists():
            return 1
        else:
            return 0

    def __str__(self):
        return self.title

    def update_continue_complete(self):
        if self.continue_complete == 0:  # 완료인 대회인지 판별
            if (date.today() - self.deadline).days >= 0:
                self.continue_complete = 1
                self.save()


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

    like = models.ManyToManyField(User, related_name='compost_likes', null=True, blank=True)

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
    like = models.ManyToManyField(User, related_name='comcomment_likes', null=True, blank=True)


# 결투장 code Post
class CodePost(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # code 업로드 한 개인

    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recommend = models.IntegerField(null=True, blank=True)
    like = models.ManyToManyField(User, related_name='codepost_likes', null=True, blank=True)


# 결투장 code에 comment
class CodeComment(models.Model):
    codepost = models.ForeignKey(CodePost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # code에 comment 단 개인

    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commcomment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)  # 대댓글
    like = models.ManyToManyField(User, related_name='codecomment_likes', null=True, blank=True)


class Answer(models.Model):
    comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accuracy = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=user_answer_upload_to, null=True)

    choice_list = ((0, 0), (1, 1))

    is_selected = models.IntegerField(default=0, choices=choice_list)  # 0 == 미선택, 1 == 선택
