from marshmallow import fields, Schema, validate

from application.error import InvalidParametersError


def validate_with_schema(request, schema):
    e = schema.validate(request.json)
    if e:
        raise InvalidParametersError


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=1))


class ShortTodoSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    end_date = fields.DateTime(required=True)
    is_completed = fields.Bool()


class TodoSchema(ShortTodoSchema):
    description = fields.Str(required=True)


user_schema = UserSchema()
todo_schema = TodoSchema()
short_todo_schema = ShortTodoSchema()
