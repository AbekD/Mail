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
from .serializers import UserSerializer, SendMessageSerializer


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
        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        user_ids = serializer.validated_data['users']
        message = serializer.validated_data['message']

        users = User.objects.filter(id__in=user_ids)
        emails = [user.email for user in users if user.email]

        if not emails:
            return Response(
                {"error": "No valid email addresses found for the given users."}
            )

        try:
            send_mail(
                subject="Notification from Our System",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to send emails: {str(e)}"}
            )

        return Response({"success": f"Message sent to {len(emails)} users."})
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

