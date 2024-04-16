
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
# from flashcards import views as flashcard_views
from classes import views as classes_views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('my_courses', classes_views.my_courses, name='my_courses'),
    path('courses/enroll/', classes_views.enroll, name='enroll_course'),
    path('courses/enroll/create/', classes_views.create, name='create_course'),
    path('courses/<id>', classes_views.view, name='view_course'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', 
        redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('flashcards.urls')),

]
