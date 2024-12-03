
from django.urls import path,re_path
from userApp import views as vw 


urlpatterns = [
    re_path(r'my_profile/(?P<user_id>\d+)/',vw.myProfile,name='my_profile'),
    re_path(r'edit_profile/(?P<user_id>\d+)/',vw.editProfile,name='edit_profile'),
    re_path(r'deactivate/(?P<user_id>\d+)/',vw.deactivate,name='deactivate'),
    ]