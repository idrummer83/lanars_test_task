from rest_framework import serializers

from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth import get_user_model

from .models import Portfolio, Image, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email')


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, validators=[
            EmailValidator(message="Wrong email. Invalid symbols used."),
        ])
    password = serializers.CharField(max_length=15,
        min_length=8,
        style={"input_type": "password"},
        validators=[
            RegexValidator(
                "^[a-zA-Z0-9-_']*.{0,1}[a-zA-Z0-9-_']*$",
                message="Wrong username. Invalid symbols used.",
            )
        ],)

    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = ('id', 'email', 'password')

    def validate_email(self, email):
        try:
            get_user_model().objects.get(email=email)
            raise serializers.ValidationError('Another user has already been registered under this address.')
        except User.DoesNotExist:
            return email

    def validate(self, data):
        password = data.get('password')

        if not password:
            raise serializers.ValidationError({
                'password': 'Passwords must match.'
            })
        return data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        read_only_fields = ('id', 'created')
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        read_only_fields = ('id', 'created')
        fields = "__all__"


class PortfolioSerializer(serializers.ModelSerializer):
    image_portfolio = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        read_only_fields = ('id', 'created')
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    portfolio_user = PortfolioSerializer(many=True, read_only=True)

    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = ("id", 'username', 'email', 'portfolio_user')
