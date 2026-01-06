from marshmallow import EXCLUDE, INCLUDE, RAISE, ValidationError
from author import Author
from schema import AuthorSchema
from pprint import pprint

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

json_data_list = """
[
   {
       "id": 1,
       "name": "Alex",
       "email": "alex@mail.ru"
   },
   {
       "id": 2,
       "name": "Ivan",
       "email": "ivan@mail.ru"
   },
   {
       "id": 4,
       "name": "Tom",
       "email": "tom@mail.ru"
   }
]
"""

authors_schema = AuthorSchema(many=True)
res_one = authors_schema.loads(json_data_list, unknown=INCLUDE)
# print(f'{res_one = !r}')
pprint(res_one)

# либо так

res_one = authors_schema.loads(json_data_list, many=True, unknown=INCLUDE)
pprint(res_one, sort_dicts=False)
