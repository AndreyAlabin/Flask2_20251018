from marshmallow import EXCLUDE, INCLUDE, RAISE, ValidationError
from author import Author
from schema import AuthorSchema

json_data = """
{
    "id": 12,
    "name": "Ivan",
    "email": "ivanmail.ru",
    "age": "21"
}
"""

try:
    schema = AuthorSchema(partial=False, unknown=EXCLUDE)
    result = schema.loads(json_data, unknown=EXCLUDE)
    print(type(result), result)
except ValidationError as e:
    print(e.messages)

# r = schema.load(result)
# print(type(r), r)
# print(Author(**r))
