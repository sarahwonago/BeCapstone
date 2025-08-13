from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes user information.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["role"] = user.role
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user information to the response
        user_serializer = UserSerializer(self.user)
        data["user"] = user_serializer.data

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses the custom token serializer.
    """

    serializer_class = CustomTokenObtainPairSerializer
