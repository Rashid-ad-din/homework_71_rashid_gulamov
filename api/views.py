from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import Account
from api.serializers import PostSerializer
from posts.models import Post


class IsAllowed(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            pk = view.kwargs['pk']
            post = get_object_or_404(Post, pk=pk)
            return user == post.author
        return True


class PostView(ModelViewSet):
    permission_classes = [IsAllowed]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        PostSerializer.author = author
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Post, pk=pk)
        post_serializer = PostSerializer(instance, data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_200_OK)
        else:

            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Post, pk=pk)
        instance.delete()
        return Response(data={'result': 'Deleted successfully'}, status=status.HTTP_200_OK)


def like(request: WSGIRequest, *args, **kwargs):
    post_pk = request.GET.get('post_pk')
    account_pk = request.GET.get('account_pk')
    post = get_object_or_404(Post, pk=post_pk)
    account = get_object_or_404(Account, pk=account_pk)
    if post and account:
        post.user_likes.add(account.pk)
        response_data = {
            'result': 'The post has been successfully liked'
        }
        response = JsonResponse(response_data)
        response.status_code = 200
        return response
    response_data = {
        'error': "Wrong request"
    }
    response = JsonResponse(response_data)
    response.status_code = 400
    return response


def unlike(request: WSGIRequest, *args, **kwargs):
    post_pk = request.GET.get('post_pk')
    account_pk = request.GET.get('account_pk')
    post = get_object_or_404(Post, pk=post_pk)
    account = get_object_or_404(Account, pk=account_pk)
    if post and account:
        post.user_likes.remove(account.pk)
        response_data = {
            'result': 'The like has been successfully removed from post'
        }
        response = JsonResponse(response_data)
        response.status_code = 200
        return response
    response_data = {
        'error': "Wrong request"
    }
    response = JsonResponse(response_data)
    response.status_code = 400
    return response
