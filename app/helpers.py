from flask import flash


def toast(message, category="success"):

    flash(
        message,
        category
    )