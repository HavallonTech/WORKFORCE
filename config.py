import os


class Config:

    SECRET_KEY = 'Cisco@2026_BTHDC'

    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:P%40ssword%401@localhost/workforce_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.zoho.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = "bt.reports@bthdc.com.ng"

    MAIL_PASSWORD = "P@ssword@1."

    MAIL_DEFAULT_SENDER = "bt.reports@bthdc.com.ng"

    MAIL_TIMEOUT = 15