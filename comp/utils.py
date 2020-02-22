import os
from datetime import date
from uuid import uuid4
from comp.models import *


def join_user():
    return len(Answer.objects.all())


def user_profile_image_path(instance, filename):
    # 프로필은 MEDIA/user_<id>/<profile> 에 저장될거야. 그냥 파일명으로!
    return 'user_{}/profile'.format(instance.user.id)


def user_answer_upload_to(instance, filename):
    # 유저가 올린 답안은은 MEDIA/user_<id>/<파일명> 에 저장될거야. 유저가 올린 파일명을 랜덤으로 바꿔서!
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return 'comp_{}/user_{}/{}'.format(instance.comp, instance.user, uuid_name[:2] + filename)


def comp_answer_upload_to(instance, filename):
    # 대회의 정답은 MEDIA/comp_<대회명>/<파일명> 에 저장될거야. 유저가 올린 파일명을 랜덤으로 바꿔서!
    extension = os.path.splitext(filename)[-1].lower()
    return 'comp_{}/{}'.format(instance.id, str(instance.id) + '_answer_sheet' + extension)


def date_percent(comp):
    total = (comp.deadline - comp.created_at).days
    interval = (date.today() - comp.created_at).days
    if interval < 0 or total <= 0:
        percent = 100
    else:
        percent = round(interval / total, 2) * 100
    return percent
