import os
from uuid import uuid4
from comp.models import *


def user_profile_image_path(instance, filename):
    # 프로필은 MEDIA/user_<id>/<profile> 에 저장될거야. 그냥 파일명으로!
    return 'user_{}/profile'.format(instance.user.id)


def user_answer_upload_to(instance, filename):
    # 유저가 올린 답안은은 MEDIA/user_<id>/<파일명> 에 저장될거야. 유저가 올린 파일명을 랜덤으로 바꿔서!
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return 'user_{}/{}/{}'.format(instance.user.id, filename, uuid_name[:2] + extension)

