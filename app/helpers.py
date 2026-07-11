from flask import flash
from app.models import User


def toast(message, category="success"):

    flash(
        message,
        category
    )
def generate_staff_id():
    """
    Generate the next Staff ID in the format:
    000001, 000002, 000003...
    """

    last_user = User.query.order_by(User.id.desc()).first()

    if not last_user or not last_user.staff_id:
        return "000001"

    try:
        next_number = int(last_user.staff_id) + 1
    except ValueError:
        next_number = last_user.id + 1

    return f"{next_number:06d}"