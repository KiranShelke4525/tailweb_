from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('add_or_update_student/', views.add_or_update_student, name='add_or_update_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('update_student/', views.update_student, name='update_student'),
    path('logout/', views.logout_view, name='logout'),
]
