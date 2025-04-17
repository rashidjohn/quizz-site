from django.urls import path
from .views import index, ready_to_test, test, checktest, new_question, new_test
from .user_views import signup, profile

urlpatterns = [
    path('', index, name='index'),
    path('test/<int:test_id>/ready/', ready_to_test, name='ready_to_test'),
    path('test/<int:test_id>/', test, name='test'),
    path('checktest/<int:checktest_id>/', checktest, name='checktest'),
    path('new_test/', new_test, name='new_test'),
    path('test/<int:test_id>/new_question/', new_question, name='new_question'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
]