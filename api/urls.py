from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views.comments import CommentView
from api.views.posts import unlike, like, PostView

router = routers.DefaultRouter()
router.register('posts', PostView)
router.register('comments', CommentView)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('like/', like, name='like'),
    path('unlike/', unlike, name='unlike'),
]
