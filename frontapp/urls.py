from django.urls import path
from .views import (home_view, make_notes, view_notes, 
                    login_view,
                    register_view, profile_view,
                    delete_profile, all_members,
                    delete_post, edit_post)

urlpatterns = [
    path('', home_view, name='home'),
    path('make/', make_notes, name='make'),
    path('view/', view_notes, name='view'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='adduser'),
    path('profile/', profile_view, name='profile'),
    path('delete/', delete_profile, name='delete'),
    path('members/', all_members, name='members'),
    path('delpost/<int:id>/', delete_post, name='delpost'),
    path('editpost/<int:id>/', edit_post, name='editpost'),
]
