from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import (CASCADE, PROTECT, BooleanField, CharField,
                              DecimalField, EmailField, FileField, ForeignKey,
                              Model, PositiveSmallIntegerField, TextField)


class Course(Model):
    title = CharField(max_length=128)
    short_description = TextField()
    description = TextField()
    cost = DecimalField(max_digits=8, decimal_places=2)

    def purchased(self, user):
        if user.is_authenticated and __class__.objects.filter(
                order__user__id=user.id, order__payed=True,
                id=self.id).exists():
            return True
        return False


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE)
    order = PositiveSmallIntegerField()
    title = CharField(max_length=128)
    description = TextField()
    video = FileField()
    addon = FileField(null=True, blank=True)


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, *args, **kwargs):
        return True

    def has_module_perms(self, *args, **kwargs):
        return True

    def courses(self):
        return Course.objects.filter(order__user__id=self.id,
                                     order__payed=True).all()


class Order(Model):
    course = ForeignKey(Course, on_delete=PROTECT)
    user = ForeignKey(User, on_delete=CASCADE)
    payed = BooleanField(default=False)
