from django.urls import path

from accounts.views import LoginView, logout_view, RegisterView, ProfileView, UserChangeView, ProfilesView
from posts.views import PostView, PostCreateView, CommentCreateView, LikesView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profiles/', ProfilesView.as_view(), name='profiles'),
    path('profile/<int:pk>/change/', UserChangeView.as_view(), name='change'),
    path('profile/<int:upk>/posts/<int:pk>/', PostView.as_view(), name='profile_post'),
    path('profile/<int:upk>/posts/add-post/', PostCreateView.as_view(), name='post_create'),
    path('profile/<int:upk>/posts/<int:pk>/add-comment', CommentCreateView.as_view(), name='add_comment'),
    path('profile/<int:upk>/posts/<int:pk>/likes/', LikesView.as_view(), name='post_likes')
]
