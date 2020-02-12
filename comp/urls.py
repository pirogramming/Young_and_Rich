from django.urls import path
from . import views
from .views import progressbar

# from .utils import progressbar

app_name = 'comp'

urlpatterns = [
    path("", views.comp_list, name="comp_list"),
    path("<int:pk>/overview/", views.comp_detail_overview, name="comp_overview"),
    path("<int:pk>/overview/description", views.comp_detail_overview_description, name="comp_description"),
    path("<int:pk>/overview/evaluation", views.comp_detail_overview_evaluation, name="comp_evaluation"),
    path("<int:pk>/overview/timeline", views.comp_detail_overview_timeline, name="comp_timeline"),
    path("<int:pk>/overview/prizes", views.comp_detail_overview_prizes, name="comp_prizes"),

    path("<int:pk>/data/", views.comp_detail_data, name="comp_data"),

    # community
    path("<int:pk>/community/", views.comp_detail_community_list, name="comp_community_list"),
    path("<int:pk>/community/<int:pk2>/", views.comp_detail_community_detail, name="comp_community_detail"),

    path("<int:pk>/community/create/", views.comp_detail_community_post_create, name="comp_community_post_create"),
    path("<int:pk>/community/<int:pk2>/update/", views.comp_detail_community_post_update,
         name="comp_community_post_update"),
    path("<int:pk>/community/<int:pk2>/delete/", views.comp_detail_community_post_delete,
         name="comp_community_post_delete"),

    path("<int:pk>/community/<int:pk2>/create/", views.comp_detail_community_comment_create,
         name="comp_community_comment_create"),
    path("<int:pk>/community/<int:pk2>/<int:pk3>/update/", views.comp_detail_community_comment_update,
         name="comp_community_comment_update"),
    path("<int:pk>/community/<int:pk2>/<int:pk3>/delete/", views.comp_detail_community_comment_delete,
         name="comp_community_comment_delete"),

    path("<int:pk>/community/<int:pk2>/<int:pk3>/create/", views.comp_detail_community_commcomment_create,
         name="comp_community_commcomment_create"),
    path("<int:pk>/community/<int:pk2>/<int:pk3>/<int:pk4>/delete/", views.comp_detail_community_commcomment_delete,
         name="comp_community_commcomment_delete"),

    # code
    path("<int:pk>/code/", views.comp_detail_code_list, name="comp_code_list"),
    path("<int:pk>/code/<int:pk2>/", views.comp_detail_code_detail, name="comp_code_detail"),

    path("<int:pk>/code/create/", views.comp_detail_code_post_create, name="comp_code_create"),
    path("<int:pk>/code/<int:pk2>/update/", views.comp_detail_code_post_update, name="comp_code_update"),
    path("<int:pk>/code/<int:pk2>/delete/", views.comp_detail_code_detail, name="comp_code_delete"),

    path("<int:pk>/code/<int:pk2>/create/", views.comp_detail_code_comment_create,
         name="comp_code_comment_create"),
    path("<int:pk>/code/<int:pk2>/<int:pk3>/update/", views.comp_detail_code_comment_update,
         name="comp_code_comment_update"),
    path("<int:pk>/code/<int:pk2>/<int:pk3>/delete/", views.comp_detail_code_comment_delete,
         name="comp_code_comment_delete"),

    path("<int:pk>/community/<int:pk2>/<int:pk3>/create/", views.comp_detail_code_commcomment_create,
         name="comp_code_commcomment_create"),
    path("<int:pk>/community/<int:pk2>/<int:pk3>/<int:pk4>/delete/", views.comp_detail_code_commcomment_delete,
         name="comp_code_commcomment_delete"),

    # rank
    path("<int:pk>/ranking/", views.comp_ranking, name="comp_ranking"),

    # explanation
    path("explanation/page", views.comp_explanation_page, name="explanation_page"),
    path("explanation/competition", views.comp_explanation_competition, name="explanation_competition"),
    path("explanation/FAQ", views.comp_explanation_faq, name="explanation_faq"),

    # path("<int:pk>/submit/", views.submit_answer, name="comp_submit_answer"),
    # path("<int:pk>/answerlist/", views.answer, name="comp_answerlist"),
    path('<int:pk>/progressbar/', progressbar, name='progressbar'),

    path('createcomp/', views.create_comp, name="create_comp"),
]
