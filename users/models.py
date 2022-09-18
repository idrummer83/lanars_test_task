from django.db import models
from django.contrib.auth.hashers import (make_password,)
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True, verbose_name='user_email')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='user_name', unique=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_user')
    name = models.CharField(max_length=150, verbose_name='portfolio_name')
    description = models.TextField(verbose_name='portfolio_description', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')

    class Meta:
        verbose_name = 'Portfolio'
        ordering = ['-created']

    def __str__(self):
        return self.name


class Image(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='image_portfolio')
    name = models.CharField(max_length=150, verbose_name='image_name')
    description = models.CharField(max_length=500, verbose_name='image_description', blank=True, null=True)
    image = models.ImageField(upload_to="images", blank=True, null=True, verbose_name='image')
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')

    class Meta:
        verbose_name = 'Image'
        ordering = ['-created']

    def __str__(self):
        return f"{self.id} - {self.name}"


class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comment_image')
    text = models.CharField(max_length=250, verbose_name='comment_text')
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')

    class Meta:
        verbose_name = 'Comment'
        ordering = ['-created']

    def __str__(self):
        return self.text
