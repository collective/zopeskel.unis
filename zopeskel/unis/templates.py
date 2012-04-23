import copy
import os

from zopeskel.unis.abstract_buildout import AbstractBuildout

from zopeskel.base import BaseTemplate
from zopeskel.base import var, EASY, EXPERT
from zopeskel.vars import StringVar, BooleanVar, IntVar, OnOffVar, BoundedIntVar, StringChoiceVar

#--------------------------------------
#   Allows to choose the customer name
#--------------------------------------

VAR_CUSTOMER = StringVar(
    'customer',
    title='Customer name',
    description='',
    default='',
    modes=(EASY,EXPERT),
    page='Main',
    help="""
This is the customer name.
"""
    )

#--------------------------------------
#   Allows to choose the Domain name
#--------------------------------------

VAR_DOMAIN = StringVar(
    'domain_name',
    title='Domain name',
    description="Domain name that will be used to access to your Plone",
    default='dev.plone.localdomain',
    modes=(EASY, EXPERT),
    page='Main',
    help="""
This is the domain name used to access from external resources to your Plone throught proxy.
eg: type preproduction.project.plone.yourdomain.com for http://preproduction.project.plone.yourdomain.com
"""
    )

#--------------------------------------
#   Allows to choose the Plone site id
#--------------------------------------

VAR_PLONESITE_PATH = StringVar(
    'plonesite_path',
    title='Plonesite id in the Zope root',
    description="Domain name that will be used to access to your Plone",
    default='site',
    modes=(EASY, EXPERT),
    page='Main',
    help="""
This is the id of the plone site object in Zope. It is used for
"""
    )

#--------------------------------------
#   Allows to choose the Plone version
#--------------------------------------

VAR_PLONEVER = StringVar(
    'plone_version',
    title='Plone Version',
    description='Plone version # to install',
    default='4-latest',
    modes=(EASY, EXPERT),
    page='Main',
    help="""
This is the version of Plone that will be used for this buildout.
You should enter the version number you wish to use.
"""
    )

#------------------------------------------
#   Allows to choose the deployment profile
#------------------------------------------

VAR_BUILDOUT_PROFILE = StringChoiceVar(
    'buildout_profile',
    title='Buildout Default Profile',
    description='The profile use by default when you will run buildout for the first time',
    default='development',
    choices=('development', 'standalone', 'production', 'preproduction', 'local_preproduction'),
    modes=(EASY, EXPERT),
    page='Main',
    help="""
You can choose the profile that is use when you will run buildout.
Option are:
- development (default)
- standalone (No ZEO)
- production (ZEO with 2 instances)
- preproduction (ZEO with 1 instance)
- local_preproduction (ZEO with 1 instance for local servers)
"""
    )

VAR_INSTANCE_TYPE = StringChoiceVar(
    'instance_type',
    title='Instance Type',
    description='How do you want to store your ZODB?',
    page='Main',
    modes=(EXPERT,),
    default='filestorage',
    choices=('filestorage','relstorage'),
    help="""
This option lets you select your ZODB storage mode.
The RelStorage store all data in a relational database instead of a single file.
Database supposed to work: PostgreSQL, Oracle, MySQL.
"""
    )

VAR_INSTANCE_ENUM = BoundedIntVar( #XXX
    'instance_enum',
    title='Number of instances',
    description='Number of instances managed in the cluster',
    default='2',
    modes=(EXPERT,),
    page='Main',
    help="""
This option let you choose how many client chould be installed in this cluster.
""",
    min=1,
    max=128,
    )

VAR_SHARED_BLOBS = BooleanVar(
    'shared_blobs',
    title='Shared Blobs',
    description='Do you want to share files stored in blobstorage?',
    default='true',
    modes=(EXPERT),
    page='Main',
    help="""
By default files stored in blobs are shared throught the ZEO server connexion.
If you activate this option files will be served directly throught the filesystem
for all clients.
"""
)

VAR_MEMCACHE = BooleanVar( #XXX
    'enable_memcache',
    title='Enable memcache',
    description="Enable the memcache machinery for let zeo clients shared memory",
    default='true',
    modes=(EXPERT,),
    page='Main',
    help="""
Use a memcache server to share RAM between ZEO clients.
"""
    )

#--------------------------------------
#   Allows to define a port starting value
#--------------------------------------

VAR_PORTS_STARTING_VALUE = BoundedIntVar(
    'ports_starting_value',
    title='Ports stating value',
    description='Ports starting value use to generate buildout files',
    default='8080',
    modes=(EASY, EXPERT),
    page='Main',
    help="""
This options lets you select the ports starting value that the configuration will use to generate the instance configuration (instance,zeo,varnish,pound/squid,...).
""",
    min=1024,
    max=65535,
    )

#--------------------------------------
#   Allows to choose a cache utility
#--------------------------------------

VAR_CACHE_UTILITY = StringChoiceVar( #XXX
    'cache_utility',
    title='Cache utility',
    description='Which cache utility would you like? (Squid/Varnish)?',
    page='Main',
    modes=(EXPERT,),
    default='varnish',
    choices=('squid','varnish'),
    help="""
This option lets you select your cache utility.
It will also generate a default configuration for the utility.
""")

#--------------------------------------
#   Allows to choose a balancer utility
#--------------------------------------

VAR_BALANCER_UTILITY = StringChoiceVar(
    'balancer_utility',
    title='Balancer utility',
    description='Which balancer utility would you like? (HAProxy/Pound)?',
    page='Main',
    modes=(EXPERT,),
    default='haproxy',
    choices=('pound','haproxy'),
    help="""
This option lets you select your balancer utility.
It will also generate a default configuration for the utility.
""")

#--------------------------------------
#   Allows to choose a http utility
#--------------------------------------

VAR_HTTP_UTILITY = StringChoiceVar(
    'http_utility',
    title='Front http utility',
    description='Which front http utility would you like? (Apache/NGinx)?',
    page='Main',
    modes=(EXPERT,),
    default='apache',
    choices=('apache','nginx'),
    help="""
This option lets you select your front http utility.
It will also generate a default configuration for the utility.
""")

VAR_MUNIN = BooleanVar(
    'munin',
    title='Munin activation',
    description='Do you want munin stats for you instance',
    default='true',
    modes=(EXPERT),
    help="""
This option install and configure a Munin plugin for zope.
It supposes that the current server has a munin node installed.
"""
)

VAR_DB_TYPE = StringChoiceVar(
    'db_type',
    title='Database Connector',
    description='Which database connector we should use for RelStorage',
    page='Main',
    modes=(EXPERT,),
    default='postgresql',
    choices=('mysql', 'oracle', 'postgresql'),
    help="""
This option install the good python connector for RelStorage.
"""
    )

VAR_DB_HOST = StringVar(
    'db_host',
    title='Database Host',
    description="Database server address",
    page='Main',
    modes=(EXPERT,),
    default='127.0.0.1',
    help="""
This option should contain the ip address or the domain name of the database server
"""
    )

VAR_DB_PORT = StringVar(
    'db_port',
    title='Database Port',
    description="Database server port",
    page='Main',
    modes=(EXPERT,),
    default='5432',
    help="""
This option should contain the port of the database server
"""
    )

VAR_DB_USERNAME = StringVar(
    'db_username',
    title='Database Username',
    description="Database username",
    page='Main',
    modes=(EXPERT,),
    default='plone',
    help="""
"""
    )

VAR_DB_PASSWORD = StringVar(
    'db_password',
    title='Database Password',
    description="Database password",
    page='Main',
    modes=(EXPERT,),
    default='azerty',
    help="""
"""
    )

VAR_APP_LDAP = BooleanVar(
    'app_ldap',
    title='Install LDAP features',
    description='Do you want to connect a LDAP annuary?',
    default='false',
    modes=(EXPERT),
    help="""
This option install all needed LDAP products for Plone.
It supposes that the current server has a python-ldap installed.
"""
)

VAR_APP_CAS = BooleanVar(
    'app_cas',
    title='Install CAS features',
    description='Do you want to connect a CAS SSO?',
    default='false',
    modes=(EXPERT),
    help="""
This option install all needed CAS products for Plone.
"""
)

VAR_APP_METNAV = BooleanVar(
    'app_metnav',
    title='Install Metnav products',
    description='Do you want to use Metnav features?',
    default='false',
    modes=(EXPERT),
    help="""
This option install all needed metnav products for Plone.
"""
)

VAR_APP_GETPAID = BooleanVar(
    'app_getpaid',
    title='Install GetPaid products',
    description='Do you want to use GetPaid features?',
    default='false',
    modes=(EXPERT),
    help="""
This option install all needed to transform your Plone site in an e-commerce things.
"""
)

VAR_APP_THEMING = BooleanVar(
    'app_theming',
    title='Install plone.app.theming products with Diazo',
    description='Do you want to use Diazo features?',
    default='true',
    modes=(EXPERT),
    help="""
This option install all needed have Diazo theming in your plone site.
"""
)

class UnisPlone4Buildout(AbstractBuildout):
    _template_dir = 'templates/unis_plone4_buildout'
    summary = "A buildout for Plone 4.x"
    help = """
This template creates a Plone 4 buildout based on the best practices of Quadra-Informatique
"""
    pre_run_msg = """
Creating Zopeskel Plone 4.x instance
"""
    post_run_msg = """
Generation finished.

You probably want to run python bootstrap.py and then edit
buildout.cfg before running bin/buildout -v

DO NOT FORGET: IP Adresses and Ports are set by default.
-------------  You HAVE to modify them in order to avoid conflict with existing instances.

See README.txt for details.
"""
    required_templates = []
    use_cheetah = True

    port_vars = [ 'dev_instance',
                  'cache_locprep',
                  'cache_preprod',
                  'cache_prod',
                  'balancer_locprep',
                  'balancer_preprod',
                  'balancer_prod',
                  'zeoserv_locprep',
                  'zeoclient_locprep_1',
                  'zeoclient_locprep_2',
                  'zeoserv_preprod',
                  'zeoclient_preprod_1',
                  'zeoclient_preprod_2',
                  'zeoserv_prod',
                  'zeoclient_prod_1',
                  'zeoclient_prod_2',
                  'supervisor_locprep',
                  'supervisor_preprod',
                  'supervisor_prod',]

    VAR_PORTS_STARTING_VALUE.description += " (Generating %s ports )" % len(port_vars)

    vars = copy.deepcopy(AbstractBuildout.vars)
    vars.extend( [
        VAR_CUSTOMER,
        VAR_DOMAIN,
        VAR_PLONESITE_PATH,
        VAR_PLONEVER,
        VAR_BUILDOUT_PROFILE,
        VAR_INSTANCE_TYPE,
        VAR_DB_TYPE,
        VAR_DB_HOST,
        VAR_DB_PORT,
        VAR_DB_USERNAME,
        VAR_DB_PASSWORD,
        VAR_INSTANCE_ENUM,
        VAR_SHARED_BLOBS,
        VAR_MEMCACHE,
        VAR_PORTS_STARTING_VALUE,
        VAR_BALANCER_UTILITY,
        VAR_CACHE_UTILITY,
        VAR_HTTP_UTILITY,
        VAR_MUNIN,
        VAR_APP_LDAP,
        VAR_APP_CAS,
        VAR_APP_METNAV,
        VAR_APP_GETPAID,
        VAR_APP_THEMING,
    ])

    def run(self, command, output_dir, vars):
        output_dir = vars["customer"] and "%s.%s"%(str(vars["customer"]).lower(), str(vars["project"]).lower()) or  str(vars["project"]).lower()

        self.pre(command, output_dir, vars)

        current_port = int(vars["ports_starting_value"])

        for key in self.port_vars:
            vars[key] = current_port
            self.post_run_msg += '\n\t %s = %s\n' % (key, current_port)
            current_port += 1

        self.write_files(command, output_dir, vars)
        self.post(command, output_dir, vars)

    def post(self, command, output_dir, vars):
        ## XXX We should cleanup unused modules

        super(UnisPlone4Buildout, self).post(command, output_dir, vars)

