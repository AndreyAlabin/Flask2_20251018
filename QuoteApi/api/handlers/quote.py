from api import db, app
from flask import jsonify, abort, request
from api.models.quote import QuoteModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from . import check


@app.get("/quotes")
def get_quotes():
    '''2. Quotes / GET List of Quotes [Done]'''
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    quotes = []
    for quote in quotes_db:
        quotes.append(quote.to_dict())
    return jsonify(quotes), 200


@app.get("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id: int):
    '''4. Quotes / GET Quote by ID [Done]'''
    quote = db.get_or_404(QuoteModel, quote_id, description=f"Quote with id={quote_id} not found")
    return jsonify(quote.to_dict()), 200


@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    '''8. Quotes / Delete Quote by ID [Done]'''
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    db.session.delete(quote)
    try:
        db.session.commit()
        return jsonify({"message": f"Quote with id {quote_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id: int):
    '''10. Quotes / Edit Quote by ID [Done]'''
    new_data = request.json
    result = check(new_data, check_rating=True)
    if not result[0]:
        return abort(400, result[1].get('error'))
    
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")

    try:
        for key_as_attr, value in new_data.items():
            setattr(quote, key_as_attr, value)

        db.session.commit()
        return jsonify(quote.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
