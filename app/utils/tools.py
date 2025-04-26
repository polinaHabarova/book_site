from app.models import Review


def get_average_rating_book(book_id, db_session):
    book_reviews = db_session.query(Review).filter(Review.book_id == book_id).all()
    average_rating = []
    for book_review in book_reviews:
        average_rating.append(int(book_review.rating))
    average_rating = sum(average_rating) / len(average_rating)
    return average_rating

