from django.db.models import CharField, Model, TextField


class Course(Model):
    title = CharField(max_length=128)
    description = TextField()
