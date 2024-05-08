from tortoise.models import Model
from tortoise import fields
from tortoise.validators import MaxLengthValidator


class Users(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(60, null=True)
    form = fields.IntField(null=True)
    study_group = fields.CharField(100, null=True)

    def __getitem__(self, item):
        match item:
            case 0:
                return self.id
            case 1:
                return self.full_name
            case 2:
                return self.form
            case 3:
                return self.study_group

    def __setitem__(self, item, new_value):
        match item:
            case 0:
                self.id = new_value
            case 1:
                self.full_name = new_value
            case 2:
                self.form = new_value
            case 3:
                self.study_group = new_value
