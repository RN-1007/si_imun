from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username harus diisi')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser harus memiliki role admin.')
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser harus memiliki is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser harus memiliki is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    username = models.CharField(max_length=150, unique=True)
    nama = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nama']

    def __str__(self):
        return self.username

class JadwalImunisasi(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jadwal_imunisasi')
    nama_anak = models.CharField(max_length=100)
    jenis_imunisasi = models.CharField(max_length=100)
    tanggal = models.DateField()
    keterangan = models.TextField(blank=True)
    selesai = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama_anak} - {self.jenis_imunisasi}"
