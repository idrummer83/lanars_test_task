from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

from users.models import User, Portfolio, Image
from users.serializers import SignupSerializer, ProfileSerializer, PortfolioSerializer, ImageSerializer, \
    CommentSerializer


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.create_user(request.data.get("email"), request.data.get("password"))
        user.set_password(make_password(request.data.get("password")))

        refresh = RefreshToken.for_user(user)
        user_serializer = ProfileSerializer(user)
        data = {
            **user_serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=e)


class UpdateDestroyProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self, pk):
        return get_object_or_404(User, id=pk)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object(kwargs.get('pk'))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePortfolioView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortfolioSerializer


class UpdateDestroyPortfolioView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortfolioSerializer

    def get_object(self, pk):
        return get_object_or_404(Portfolio, id=pk)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object(kwargs.get('pk'))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePortfolioImageView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer


class UpdateDestroyPortfolioImageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_object(self, pk):
        return get_object_or_404(Image, id=pk)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object(kwargs.get('pk'))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateImageCommentView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer


class ImageListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name', '$description', 'portfolio__name']
    ordering_fields = ['created']

