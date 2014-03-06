djorm-ext-pgtrgm
================

Django pgtrgm is a Django application with some addons regarding PostgreSQL trigram
(or trigraph) text comparison

A trigram is a group of three consecutive characters taken from a string. We can
measure the similarity of two strings by counting the number of trigrams they share.
This simple idea turns out to be very effective for measuring the similarity of words
in many natural languages.

For example, the set of trigrams in the string "cat" is " c", " ca", "cat", and "at ".

With this extension, we could use this feature inside Django ORM with a simple
QuerySet filter keyword

It is distributed under the terms of the [GNU Lesser General Public
License](http://www.gnu.org/licenses/lgpl.html)

PostgreSQL syntax
-----------------

`text % text` -> boolean Returns true if its arguments have a similarity that is greater
than the current similarity threshold set by set_limit.

[How to install and use pg_trgm extension in PostgreSQL 9.2](http://www.postgresql.org/docs/9.2/static/pgtrgm.html)


Requeriments
------------

- Django 1.5 (or higher). It's possible that works with other versions lower 1.5
- Postgres `pg_trgm` extension. In debian/ubuntu: `sudo apt-get install postgres-contrib`


Installation
------------

- In your `settings.py`

    INSTALLED_APPS = (

        'djorm_pgtrgm',
    )

- You need to *register* the extension in your database. Run `./manage.py dbshell` and then execute:

    CREATE EXTENSION pg_trgm;

- Optionally, you can create an index over a text column for the purpose of very fast similarity searches. For example, supose you will filter a lot over the field
`description` of the model `myapp.Product`:

    CREATE INDEX desctiption_trgm_idx ON myapp_product USING gist (description gist_trgm_ops);


Usage
-----------

Adds a new query set filter keyword to allow text searching.

    MyModel.objects.filter(field_name__similar='whatever')

To ensure results ordered by similarity, try this:

    MyModel.objects.filter(field_name__similar='whatever').
                      extra(select={'distance': "similarity(name, 'whatever')"}).
                      order_by('-distance'))

Development
-----------

You can get the last version of djorm-ext-pgtrgm by doing a clone
of its repository:

    git clone git://github.com/jleivaizq/djorm-ext-pgtrgm.git
