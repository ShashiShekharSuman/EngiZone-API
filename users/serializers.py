from asyncore import read
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from api.problems.serializers import QuestionSerializer
from .models import User, Contact


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_no', 'avatar', 'email',  'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(Serializer):
    user = UserSerializer()
    # questions = QuestionSerializer(quaryse many=True)


class LogInSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        token = super(LogInSerializer, self).validate(attrs)
        # Custom data you want to include
        # user = {
        #     'id': self.user.id,
        #     'first_name': self.user.first_name,
        #     'last_name': self.user.last_name,
        #     'email': self.user.email,
        #     'avatar': self.user.avatar,
        # }
        user = UserSerializer(self.user).data
        # and everything else you want to send in the response
        return {'token': token, 'user': user}


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
