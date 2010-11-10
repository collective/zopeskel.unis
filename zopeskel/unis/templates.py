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
#   Allows to choose the Plone version
#--------------------------------------

VAR_PLONEVER = StringVar(
    'plone_version',
    title='Plone Version',
    description='Plone version # to install',
    default='4.0.1',
    modes=(EXPERT),
    page='Main',
    help="""
This is the version of Plone that will be used for this buildout.
You should enter the version number you wish to use.
"""
    )

#--------------------------------------
#   Allows to choose the Zope version
#--------------------------------------

VAR_ZOPEVER = StringVar(
    'zope2_version',
    title='Zope2 Version',
    description='Zope version # to install',
    default='2.12.10',
    modes=(EXPERT),
    page='Main',
    help="""
This is the version of Zope that will be used for this buildout.
You should enter the version number you wish to use.
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
    modes=(EXPERT),
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

VAR_CACHE_UTILITY = StringChoiceVar(
    'cache_utility',
    title='Cache utility',
    description='Which cache utility would you like? (squid/varnish)?',
    page='Main',
    modes=(EXPERT),
    default='varnish',
    choices=('squid','varnish'),
    help="""
This option lets you select your cache utility. It will also generate a default configuration for the utility
""")

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
        VAR_ZOPEVER,
        VAR_PLONEVER,
        VAR_PORTS_STARTING_VALUE,
        VAR_CACHE_UTILITY,
    ])

    def run(self, command, output_dir, vars):

        self.pre(command, output_dir, vars)

        current_port = int(vars["ports_starting_value"])

        for key in self.port_vars:
            vars[key] = current_port
            self.post_run_msg += '\n\t %s = %s\n' % (key, current_port)
            current_port += 1

        self.write_files(command, output_dir, vars)
        self.post(command, output_dir, vars)

    def post(self, command, output_dir, vars):
        project_folder = "%s.%s"%(str(vars["customer"]).lower(), str(vars["project"]).lower())
        os.system('mv %s %s'%(output_dir, project_folder))

        super(ZopeskelPlone4Buildout, self).post(command, project_folder, vars)

