===============================
SynBio Glyph repository
===============================

A Registry of Synthetic Biology Glyphs, created for the IWBDA 2017 BDAthlon competition

It was built using Flask as a web framework, SQLAlchemy as an ORM layer, and various Flask packages (most notably
Flask-Login, WTForms and Flask-WTF, but see ``requirements/prod.txt`` for a complete list). The front-end uses Boostrap
for layout, FontAwesome for icons, jQuery as a dependendy for Bootstrap, and the selectize library for fuzzy-filtering
of lists. As a starting point, `cookiecutter-flask https://github.com/sloria/cookiecutter-flask`_ was used to create the
boilerplate for a site with user management but no other interactivity.

Project Structure
-----------------
The project consists of many files. These are some of the most significant ones ::

    autoapp.py    - main entrypoint that creates an application instance
    requirements/ - list of project requirements in format readable by ``pip -r``

    glyphrepository/
        app.py      - app factory function
        assets.py   - lists JS and CSS files to be included
        settings.py - main configuration file
        static/     - JS and CSS files, as well as the images of glyphs
        templates/  - directory of template files (in Jinja2 format)

    The bulk of the non-boilerplate code is in one of:

    comment/
    glyph/
    public/
    soterm/
    user/

which contain a ``model.py`` file (which defines a database table using SQLAlchemy), a ``forms.py`` file, and a ``views.py``
file (which defines the routes/URLs for the application, and the functions that actually handle requests).



Quickstart
----------

This project is written in Python using the Flask framework. If you have Python and pip installed, you can get the code
and install its dependencies (including Flask) ::

    git clone https://github.com/BDAthlon/2017-Triple_Helix-1
    cd glyphrepository
    pip install -r requirements/dev.txt



Before running shell commands, set the ``FLASK_APP`` and ``FLASK_DEBUG``
environment variables ::

    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1

You then need to setup the database. The repository includes a SQLite database (``dev.db``) that should `just work'
when debugging mode is enabled, but you can alternatively created the database from scratch ::

    flask db init
    flask db migrate
    flask db upgrade
    flask run


You will then also need to load the SO data in ``so.sql`` into the database.


You can then run the site using ::

    flask run

and nvaigate to ``127.0.0.1:5000`` in your favourite browser.


Deployment
----------

You need to set a secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export glyphrepository_SECRET='something-really-secret'


In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------
This project was written quickly at a hackathon, so contains few tests; only those that came with the scaffolding.

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.
