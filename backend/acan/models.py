from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import (CASCADE, PROTECT, BooleanField, CharField,
                              DecimalField, EmailField, FileField, ForeignKey,
                              Model, PositiveSmallIntegerField, TextField)


class Course(Model):
    order_int = PositiveSmallIntegerField()
    published = BooleanField(default=False)
    soon = BooleanField(default=False)
    title = CharField(max_length=128)
    image = FileField(upload_to='images/')
    short_description = TextField()
    description = TextField()
    cost = DecimalField(max_digits=8, decimal_places=2)

    def purchased(self, user):
        if user.is_authenticated and __class__.objects.filter(
                pk=self.id, order__user__id=user.id,
                order__payed=True).exists():
            return True
        return False

    def __str__(self):
        return self.title


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE)
    order = PositiveSmallIntegerField()
    title = CharField(max_length=128)
    description = TextField()
    video = FileField()
    addon = FileField(null=True, blank=True, upload_to='addons/')

    def __str__(self):
        return f'{self.order}. {self.title}'


class UserManager(BaseUserManager):

    def create_user(self, email, password, phone, first_name, last_name):
        user = self.model(email=self.normalize_email(email),
                          phone=phone,
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone, first_name, last_name):
        user = self.create_user(email, password, phone, first_name, last_name)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True)
    phone = CharField(max_length=16)
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    mailing_list = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']

    def has_perm(self, *args, **kwargs):
        return True

    def has_module_perms(self, *args, **kwargs):
        return True


class Order(Model):
    course = ForeignKey(Course, on_delete=PROTECT)
    user = ForeignKey(User, on_delete=CASCADE)
    payed = BooleanField(default=False)

    def __str__(self):
        return f'{self.user} @ {self.course}'


class Article(Model):
    order = PositiveSmallIntegerField()
    title = CharField(max_length=128)
    image = FileField(upload_to='article_images/')
    text = TextField()

    def __str__(self):
        return self.title
