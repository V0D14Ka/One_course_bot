from tortoise.models import Model
from tortoise import fields
from tortoise.validators import MaxLengthValidator


class Users(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(60, null=True)
    form = fields.IntField(null=True)
    study_group = fields.CharField(100, null=True)