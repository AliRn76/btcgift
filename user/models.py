import re
from django.db import models
# from configs.base_manager import BaseManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from config.utils import validate_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, is_admin=False):
        if not phone_number:
            raise ValueError(_('PhoneNumber must be set'))

        if (_phone_number := validate_phone_number(phone_number)) is None:
            raise ValueError(_('PhoneNumber is not valid'))

        if _user := self.model.objects.filter(phone_number=_phone_number).first():
            if not (_user.is_admin and is_admin):
                raise ValueError(_('That phone number is already taken.'))

        user = self.model(phone_number=_phone_number, last_login=timezone.now(), is_admin=is_admin)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password):
        return self.create_user(phone_number, password, is_admin=True)


class User(AbstractBaseUser):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=31,  unique=True)
    password = models.CharField(db_column='Password', max_length=63, blank=True, null=True)
    first_name = models.CharField(db_column='FirstName', max_length=15, default='')
    last_name = models.CharField(db_column='LastName', max_length=15, default='')

    is_banned = models.BooleanField(db_column='IsBanned', default=False)
    is_male = models.BooleanField(db_column='IsMale', blank=True, null=True)
    is_admin = models.BooleanField(db_column='IsAdmin', default=False)
    birth_date = models.DateTimeField(db_column='BirthDate', blank=True, null=True)
    last_login = models.DateTimeField(db_column='LastLogin', blank=True, null=True)
    date_joined = models.DateTimeField(db_column='DateJoined', auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'User'

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        return f'{self.first_name or ""} {self.last_name or ""}'.strip()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def update_last_login(self):
        self.last_login = timezone.now()  # TODO: Fix timezone ...
        self.save(update_fields=['last_login'])


class AddressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False).order_by('-id')


class Address(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=31, default='')
    address = models.CharField(db_column='Address', max_length=511)
    latitude = models.CharField(db_column='Latitude', max_length=63)
    longitude = models.CharField(db_column='Longitude', max_length=63)
    zip_code = models.CharField(db_column='ZipCode', max_length=10, blank=True, null=True)
    is_tehran = models.BooleanField(db_column='IsTehran')
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(db_column='IsDeleted', default=False)

    objects = AddressManager()

    class Meta:
        db_table = 'Address'
