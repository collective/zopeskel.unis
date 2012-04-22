========================================================
Installation of a Plone 4 architecture on Debian Squeeze
========================================================

:Info: See <https://github.com/collective/zopeskel.unis> for more informations
:Author: Encolpe DEGOUTE <encolpe.degoute@quadra-informatique.fr>
:Description: This is a "docinfo block", or bibliographic field list

Introduction
============

This installation is specific to Debian Squeeze 64bits. For this documentation
the hostname is `debian` and the network domain is `localdomain`.

This is a scalable architecture: a lot of software installed are not describe
in the basic plone installation. How is it scalable? If you
need to support more reader connections you can add more zope instances
connected to the postgresql cluster; If you need to support more writing users
you can add more postgresql servers in your cluster. If you have a simple site
a configuration with one postgresql server and two zope instances should be
enough.

You should plan half a day for the server installation with the Python 2.6.

OS Installation
===============

First steps
-----------

The installation starts from the last netinst CDROM boot.

* We choose the graphical installation with our locale language
* The network is acquired by the DHCP method
* For the disk partition choose `Assisted with LVM` then `All in a single
  partition`. This should avoid problem with too little `/tmp` partition in
  the future.
* Apply this modification and go to the next step.
* Create a simple root password to take care of a possible bug in the keyboard
  configuration.
* Create le 'Local admin' user.
* In the task selection choose : web server, SQL databases and simple
  installation. It will take times to download and install packages at this
  step.
* Install Grub
* Reboot

OS Configuration
----------------

All the following commands need to be logged as root or with sudo.

Debian Backports
~~~~~~~~~~~~~~~~

Add a file called **/etc/apt/sources.list.d/squeeze-backports.list** with the following line:

.. code-block:: bash

  deb http://backports.debian.org/debian-backports squeeze-backports main

Create a **/etc/apt/preferences** file with these three lines:

.. code-block:: bash

  Package: *
  Pin: release a=squeeze-backports
  Pin-Priority: 999

Then:
     
.. code-block:: bash

  apt-get update
  apt-get dselect-upgrade

This last command should propose you to update PostgreSQL that is the targeted
goal.

See `Debian Backports site`_ for more information.

.. _`Debian Backports site`: http://backports.debian.org/Instructions


Architecture requirement
~~~~~~~~~~~~~~~~~~~~~~~~

We will have to build zc.buildout and Python. With python we have three modules
needed everywhere: python-imaging, python-ldap and python libxml2 binding.

.. code-block:: bash

  sudo apt-get build-deps python
  sudo apt-get install build-essential libsqlite3-dev \
                       python-dev python-setuptools \
                       python-imaging python-lxml python-ldap \
                       python-celementree python-cjson \
                       libssl-dev libsasl2-dev libldap2-dev \
                       libgif-dev libjpeg62-dev libpng12-dev libfreetype6-dev \
                       libxml2-dev libxslt1-dev


*Memcached* is a ramcache helper for distributed application. We use it between
zope instances to reduce session overheads.

.. code-block:: bash

  sudo apt-get install memcached libmemcache-dev


We choose *PostgreSQL 8.4* to simplify the migration on Debian Sqeeze.

.. code-block:: bash

  sudo apt-get install python-psycopg2 postgresql-8.4 \
                       postgresql-contrib-8.4 postgresql-8.4-slony1 \
                       postgresql-server-dev-8.4 pidentd

Munin is installed by default on eash node

.. code-block:: bash

  sudo apt-get install munin munin-node


For Varnish cache server

.. code-block:: bash

  sudo apt-get install pkg-config libpcre3-dev


Plone requirements
~~~~~~~~~~~~~~~~~~

Unless python modules these requirements are there for specific needs: document
conversion to html (preview) and to text (indexing).

.. code-block:: bash

  sudo apt-get install lynx tidy xsltproc xpdf wv

Developper tools
~~~~~~~~~~~~~~~~

.. code-block:: bash

  sudo apt-get install vim-python git mercurial subversion graphviz


Python Sandbox Installation
---------------------------

This step can be optionnal if you only want to use the python installed by the
system or if you install your own python version. We recommend to build system
independant version of Python for Plone hosting to not be impacted if a system
upgrade turn into a nightmare.

Zope 2.12 used by Plone dropped the Python 2.5 support to concentrate all
effort on Python 2.6. Debian Squeeze contains this version. On the other hand
Zope 2.10 only runs with Python 2.4 that is only present in Debian Lenny.
Debian doesn't propose Python 2.4 and Python 2.6 on the same version. The Plone
Community has a buildout to build all python versions for Plone with some
dependencies.


Python installation
~~~~~~~~~~~~~~~~~~~

At this step you can choose to compile python in user space or in superuser
space.
This buildout expect setuptools is installed at least at 0.6.11 version.

.. code-block:: bash

  sudo adduser --home /opt/python-envs --disabled-password plone
  sudo easy_install -U setuptools
  sudo easy_install zc.buildout==1.4.4
  sudo mkdir /opt/python /opt/python-envs
  sudo chown plone:plone /opt/python /opt/python-envs
  sudo -H -u plone -s
  svn checkout http://svn.plone.org/svn/collective/buildout/python
  cd python
  python bootstrap.py
  bin/buildout


We will need to have a virtualenv installed in there to be able to duplicate
Python2.6 installation quickly.

.. code-block:: bash

  cd /opt/python/python-2.6
  source bin/activate
  easy_install virtualenv


Finalization
------------

As Zope, varnish and HAproxy don't need superuser rights we must create an user
to install the application in the userspace. You should call it `zope` or
`plone`.

The next step is to install zopeskel.unis to deploy your project.

If you want to be able to store ZODB in a PostgreSQL database you should  create
an user in your postgres database

.. code-block:: bash

  sudo -u postgres createuser -e -d -i -l -P -R -S  plone
