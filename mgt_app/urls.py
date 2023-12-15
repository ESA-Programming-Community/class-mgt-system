from django.urls import path
from . import views
from .auth import authviews
from . import quiz_views
from . import instructor_views
from . import assignments


urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', authviews.sign_up, name='signup'),
    path('login/', authviews.login_page, name='login'),
    path('logout', authviews.logout_page, name='logout'),

    path('join_community/<str:community_name>', views.join_community, name='join_community'),
    path('dashboard/<str:community_name>', views.dashboard, name='dashboard'),
    path('module_details/<str:community_name>/<str:module_name>', views.module_details, name='module_details'),
    path('resources/<str:community_name>/<str:module_name>/<str:lesson_title>', views.lesson_resources, name='lesson_resources'),
    path('delete_lesson/<str:community_name>/<str:lesson_name>', views.delete_lesson, name='delete_lesson'),
    path('<str:community_name>/resource_link_player/<int:pk>', views.lesson_resource_player, name='player'),

    path('<str:community_name>/quizzes', quiz_views.quiz_page, name='quiz_page'),
    path('<str:community_name>/quizzes/<str:quiz_title>', quiz_views.quiz_detail, name='quiz_detail'),
    path('elevated/<str:community_name>/add_quiz', quiz_views.add_quiz, name='add_quiz'),
    path('elevated/<str:community_name>/manage_quiz', quiz_views.quiz_manager, name='manage_quiz'),
    path('elevated/<str:community_name>/edit_quiz/<int:pk>', quiz_views.edit_quiz, name='edit_quiz'),
    path('elevated/<str:community_name>/change_quiz_status/<int:pk>', quiz_views.change_quiz_stat, name='quiz_stat'),
    path('elevated/<str:community_name>/<int:pk>/student_scores', quiz_views.student_quiz_scores, name='quiz_scores'),
    path('elevated/<str:community_name>/quiz/add_questions/<int:quiz_id>', quiz_views.add_question, name='add_question'),
    path('elevated/<str:community_name>/quiz/<str:quiz_title>/edit_question/<int:question_id>', quiz_views.edit_quiz_question, name='edit_question'),
    path('elevated/<str:community_name>/quiz/<str:quiz_title>/quiz_questions', quiz_views.display_quiz_question, name='quiz_questions'),
    path('elevated/<str:community_name>/assignments/add_assignments', assignments.add_assignment, name='add_assignment'),
    path('elevated/<str:community_name>/assignments/manage_assignments', assignments.manage_assignments, name='manage_assignment'),

    path('<str:community_name>/quizzes/<str:quiz_title>/summary', quiz_views.quiz_score_page, name='quiz_summary'),


    path('elevated/admin/assign_instructors', instructor_views.assign_instructor, name='assign_instructor'),
    path('elevated/admin/all_instructors', instructor_views.instructors_list, name='all_instructors'),
    path('elevated/admin', views.admin_page_duties, name='admin_page'),
]



