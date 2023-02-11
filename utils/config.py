import os


def database_config():
    """return the database url"""
    database_url = os.getenv('URL')
    database_user = os.getenv('POSTGRES_USER')
    database_pw = os.getenv('POSTGRES_PW')
    database_db = os.getenv('POSTGRES_DB')
    postgres_url = os.getenv('POSTGRES_URL')

    if postgres_url:
        return postgres_url
    else:
        return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=database_user, pw=database_pw,
                                                                     url=database_url,
                                                                     db=database_db)


def email_config(app):
    """configuration of the mail services"""
    # Setup Flask mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
