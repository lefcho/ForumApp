from django.urls import path, include
from ForumApp.posts import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add-post/', views.AddPostView.as_view(), name='add-post'),
    path('<int:pk>/', include([
        path('delete-post/', views.DeletePostView.as_view(), name='delete-post'),
        path('details-post/', views.detail_post, name='details-post'),
        path('edit-post/', views.EditPostView.as_view(), name='edit-post'),
    ]))
]
