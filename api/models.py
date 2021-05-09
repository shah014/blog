from django.db import models
from django.dispatch import receiver     # --> reset password begin
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.tokens import BaseTokenGenerator
from django.core.mail import send_mail   # --> reset password end


# step4: create a Post model and define it's fields -->step6 serializers.py


class Post(models.Model):  # step4
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    # Here foreign key at owner creates many-to-one relation
    # One user can be the owner of many post but each post can have just one user

    class Meta:
        ordering = ['created']
# This list of post will be added to UserSerializer to complete many-to-one relation
# Also, don't forget to register it in admin site


# for password reset when you forget


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email])


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=200)
