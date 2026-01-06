from author import Author
from schema import AuthorSchema
from pprint import pprint

author = Author(1, "Alex", "alex5@mail.ru")
author_schema = AuthorSchema()
result = author_schema.dump(author)
print(type(result), result)


authors_list = [
   Author("1", "Alex"),
   Author("1", "Ivan"),
   Author("1", "Tom")
]

authors_schema = AuthorSchema(many=True)
result = authors_schema.dump(authors_list)  # dump / dumps
pprint(result, sort_dicts=False)

# либо так

result = authors_schema.dump(authors_list, many=True)
pprint(repr(result))