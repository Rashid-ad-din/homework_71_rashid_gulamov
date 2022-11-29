from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import Account
from api.serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comments


class IsAllowed(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            pk = view.kwargs['pk']
            comment = get_object_or_404(Comments, pk=pk)
            print(comment.author, user)
            return user == comment.author
        return True


class CommentView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAllowed]
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        CommentSerializer.author = author
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Comments, pk=pk)
        serializer = CommentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Comments, pk=pk)
        instance.delete()
        return Response(data={'result': 'Deleted successfully'}, status=status.HTTP_200_OK)
