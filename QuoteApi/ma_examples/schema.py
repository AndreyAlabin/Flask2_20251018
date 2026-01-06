from marshmallow import Schema, fields

class AuthorSchema(Schema):
    id = fields.Integer(required=True, strict=True, dump_only=True)
    name = fields.String(required=True, error_messages={"required": "Please enter a name"})
    surname = fields.String(required=False)
    email = fields.Email(required=True, error_messages={"required": "Please enter a email"})
