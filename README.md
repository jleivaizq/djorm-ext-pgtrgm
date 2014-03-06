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

Django 1.5 (or higher). It's possible that works with other versions lower 1.5


Installation
------------

In your settings.py

    INSTALLED_APPS = (

        'djorm_pgtrgm',
    )

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
