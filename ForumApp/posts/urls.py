from django.urls import path, include
from ForumApp.posts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-post/', views.add_post, name='add-post'),
    path('<int:pk>/', include([
        path('delete-post/', views.delete_post, name='delete-post'),
        path('details-post/', views.detail_post, name='details-post'),
        path('edit-post/', views.edit_post, name='edit-post'),
    ]))
]
