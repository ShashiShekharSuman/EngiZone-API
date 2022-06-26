# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
# from django.contrib.auth.models import User
from rest_framework.decorators import action
from .serializers import ContactSerializer, UserSerializer, LogInSerializer
# from rest_framework.decorators import action
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.core.mail import send_mail, BadHeaderError
from .models import User
from django.conf import settings
# Create your views here.


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'create': [AllowAny],
        'retrieve': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        # 'bookmarks': [IsAuthenticated, IsOwnerOrReadOnly]
    }
    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=["get"])
    # def bookmarks(self, request):
    #     user = request.user
    #     serializer = BookmarkSerializer(user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class AuthenticatedUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# SAFE_METHODS = ['POST']


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
    # permission_classes_by_method = {'GET': [IsAuthenticated]}

    # def get(self, request):
    #     print(request.method, self.request.user.is_authenticated)
    #     user = {
    #         # 'id': request.user.id,
    #         # 'first_name': request.user.first_name,
    #         # 'last_name': request.user.last_name,
    #         # 'email': request.user.email
    #     }
    #     return Response(user)

    # def get_permissions(self):
    #     try:
    #         # return permission_classes depending on `method`
    #         return [permission() for permission in self.permission_classes_by_method[self.request.method]]
    #     except KeyError:
    #         # method is not set return default permission_classes
    #         return [permission() for permission in self.permission_classes]


class ContactView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            try:
                send_mail(subject, message,
                          settings.EMAIL_HOST_USER, [email, ])
                serializer.save()
            except BadHeaderError:
                return Response({'detail': 'Invalid Header Found'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
