from comp.models import *
from core.models import *


def count_user():
    # User.objects.all().count()
    # return User.objects.all().count()
    return len(User.objects.all())


def count_company():
    return len(Profile.objects.filter(is_id=1))


def count_competition():
    return len(Comp.objects.all())


def count_code():
    all_code_list = Comp.objects.all()
    code_list = ComPost.objects.all()
    a = len(code_list)
    for i in all_code_list:
        a += 1

        return a


def count_prize():
    c = Comp.objects.all()
    all_prize = 0
    for i in c:
        all_prize += i.prize

    return all_prize
