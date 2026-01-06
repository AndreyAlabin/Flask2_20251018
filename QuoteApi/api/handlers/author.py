from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


@app.get("/authors")
def get_authors():
    '''1. Authors / GET List of Authors'''
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    authors = [author.to_dict() for author in authors_db]
    return jsonify(authors), 200


@app.get("/authors/<int:author_id>")
def author_quotes(author_id: int):
    '''3. Authors / GET Author by ID [Done]'''
    author = db.get_or_404(AuthorModel, author_id, description=f'Author with id={author_id} not found')
    return jsonify(author.to_dict()), 200


@app.post("/authors")
def create_author():
    '''5. Authors / Create new Author [Done]'''
    data = request.json
    try:
        author = AuthorModel(**data)
        db.session.add(author)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <name>, <surname>. Received: {', '.join(data.keys())}.")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(author.to_dict()), 201


@app.post("/authors/<int:author_id>/quotes")
def create_quote(author_id: int):
    '''6. Quotes / Create new Quote by Author ID [Done]'''
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")
    data = request.json
    try:
        quote = QuoteModel(author, **data)
        db.session.add(quote)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <author>, <text>, <rating>. Received: {', '.join(data.keys())}.")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(quote.to_dict()), 201


@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    '''7. Authors / Delete Author by ID [Done]'''
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify({"message": f"Author with id {author_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.put("/authors/<int:author_id>")
def edit_author(author_id: int):
    '''9. Authors / Edit Author by ID [Done]'''
    new_data = request.json

    if not new_data:
        return abort(400, "No valid data to update")
    
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

    try:
        for key_as_attr, value in new_data.items():
            # if not hasattr(author, key_as_attr):
            #     raise Exception(f"Invalid key='{key_as_attr}'. Valid only {tuple(vars(author).keys())}")
            setattr(author, key_as_attr, value)

        db.session.commit()
        return jsonify(author.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.get("/authors/<int:author_id>/quotes")
def get_quote_by_author_id(author_id: int):
    '''11. Quotes / GET List of Quotes by Author ID [Done]'''
    quotes_db = db.session.scalars(db.select(QuoteModel).where(QuoteModel.author_id == author_id)).all()
    quotes_list = [q.to_dict() for q in quotes_db]
    return jsonify(quotes_list), 200
