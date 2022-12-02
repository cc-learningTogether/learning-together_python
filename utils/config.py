import distutils
import os


def database_config():
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
    # Setup Flask mail
    mail_use_ssl = os.getenv('MAIL_USE_SSL')
    try:
        if distutils.util.strtobool(os.getenv('MAIL_USE_SSL')) == 0:
            mail_use_ssl = False
        elif distutils.util.strtobool(os.getenv('MAIL_USE_SSL')) == 1:
            mail_use_ssl = True
    except ValueError:
        print("MAIL_USE_SSL value must be True or False")

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_SSL'] = mail_use_ssl
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
