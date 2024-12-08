from django.forms import model_to_dict
from pyexpat.errors import messages
from rest_framework import generics, viewsets
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from sqlalchemy import delete

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    #queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return User.objects.all()

        return User.objects.filter(pk=pk)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        user_ids = request.data.get("users")
        message = request.data.get("message")

        if not user_ids or not message:
            return Response(
                {"error": "Users and message are required fields"},
            )

        users = User.objects.filter(id__in=user_ids)

        if not users.exists():
            return Response(
                {"error": "No users found for provided IDs"},
            )

        for user in users:
            send_mail(
                subject="Notification",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            user.message = message
            user.save()

        return Response(
            {"success": f"Emails sent to {len(users)} users and messages updated."},
        )
# class UserAPIList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserAPIUpdate(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

