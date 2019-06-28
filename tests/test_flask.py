from flask import Flask

from dynaconf.contrib import FlaskDynaconf
from example.flask_with_dotenv.app import app as flask_app


def test_flask_dynaconf(settings):
    """
    Test Flask app wrapped with FlaskDynaconf
    """
    app = Flask(__name__)
    app.config["MY_VAR"] = "foo"
    FlaskDynaconf(app, dynaconf_instance=settings)
    assert app.config.HOSTNAME == "host.com"
    assert app.config.MY_VAR == "foo"

    assert app.config["HOSTNAME"] == "host.com"
    assert app.config["MY_VAR"] == "foo"

    assert app.config.get("HOSTNAME") == "host.com"
    assert app.config.get("MY_VAR") == "foo"

    assert app.config("HOSTNAME") == "host.com"
    assert app.config("MY_VAR") == "foo"


def test_flask_with_dot_env():
    envvars = {
        "HELLO": "hello flask",
        "INTVAR": 42,
        "FLOATVAR": 4.2,
        "BOOLVAR": True,
        "JSONVAR": ["flask", "rocks"],
    }
    for key, value in envvars.items():
        assert flask_app.config[key] == value


def test_flask_dotenv_cli():
    with flask_app.test_client() as client:
        assert client.get("/test").data == b"hello flask"

def test_flask_dynaconf_set_update(settings):
    app = Flask(__name__)
    settings['MY_VAR'] = "1"
    FlaskDynaconf(app, dynaconf_instance=settings)
    
    assert settings['MY_VAR'] == "1"
    assert app.config['MY_VAR'] == "1"
    
    settings.set('MY_VAR', '2')
    assert settings['MY_VAR'] == "2"
    assert app.config['MY_VAR'] == "2"

    app.config.set('MY_VAR', '3')
    assert settings['MY_VAR'] == "3"
    assert app.config['MY_VAR'] == "3"

    settings.update({'MY_VAR': '4'})
    assert settings['MY_VAR'] == "4"
    assert app.config['MY_VAR'] == "4"

    app.config.update({'MY_VAR': '5'})
    assert settings['MY_VAR'] == "5"
    assert app.config['MY_VAR'] == "5"

def test_manually_overriding_flask_conf_settings(settings):
    app = Flask(__name__)

    # initialize dynaconf settings instance with a message value
    settings["MESSAGE"] = "hello"
    # assert that the value is set correctly
    assert settings["MESSAGE"] == "hello"

    # tie the dyanconf settings and flask app config together
    FlaskDynaconf(app, dynaconf_instance=settings)

    # assert that the message value is unchanged
    assert app.config["MESSAGE"] == "hello"
    assert settings.MESSAGE == "hello"

    # change the value manually via dynaconf settings instance
    settings["MESSAGE"] = "bye"

    # assert that the value is changed
    assert settings["MESSAGE"] == "bye"
    assert app.config["MESSAGE"] == "bye"

    # change the value manually via app.config
    app.config["MESSAGE"] = "hi"

    # assert that the value is changed
    assert app.config["MESSAGE"] == "hi"
    assert settings["MESSAGE"] == "hi"

    # update the value via settings using a dictionary
    message_dict = {"MESSAGE": "ay"}
    settings.update(message_dict)
    # assert the value is updated
    assert settings["MESSAGE"] == "ay"

    # update the value via app.config using a dictionary
    message_dict = {"MESSAGE": "yo"}
    app.config.update(message_dict)
    # assert the value is updated
    assert app.config["MESSAGE"] == "yo"
    # above fails because the update method does not work properly