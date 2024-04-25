
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from files.views import serve_file
from classes import views as classes_views
from social.views import request_friendship, respond_to_friend_request

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('my_courses', classes_views.my_courses, name='my_courses'),
    path('courses/enroll/', classes_views.enroll, name='enroll_course'),
    path('courses/enroll/create/', classes_views.create, name='create_course'),
    path('courses/<id>', classes_views.view, name='view_course'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('flashcards.urls')),
    path('users/', include('allauth.urls')),
    path('flashcards/', include('flashcards.urls')),
    path('files/', include('files.urls')),
    path('serve_file/<int:file_id>', serve_file, name='serve_file'),
    path('request_friendship/<friend_name>', request_friendship, name='request_friendship'),
    path('friend_respond/<friend_name>/<status>', respond_to_friend_request, name='friend_respond'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)