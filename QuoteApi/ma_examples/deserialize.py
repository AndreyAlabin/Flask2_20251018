from marshmallow import EXCLUDE, INCLUDE, RAISE, ValidationError
from author import Author
from schema import AuthorSchema

json_data = """
{
    "id": 2,
    "name": "Ivan",
    "email": "ivan@mail.ru"
}
"""

try:
    schema = AuthorSchema(partial=False)  # unknown=EXCLUDE
    result = schema.loads(json_data, unknown=INCLUDE) # unknown=EXCLUDE
    print(type(result), result)
except ValidationError as e:
    print(e.messages)

r = schema.load(result, unknown=INCLUDE) # unknown=EXCLUDE
print(type(r), r)
print(Author(**r))
