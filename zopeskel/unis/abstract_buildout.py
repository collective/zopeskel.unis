import copy
import os

from zopeskel.base import BaseTemplate
from zopeskel.base import var, EASY, EXPERT
from zopeskel.vars import StringVar, BooleanVar, IntVar, OnOffVar, BoundedIntVar

#----------------------------------------------------------------------------------------
#   Old vars...

VAR_ZOPE_USER = StringVar(
    'zope_user',
    title='Initial Zope Username',
    description='Username for Zope root admin user',
    modes=(EXPERT),
    page='Main',
    default='admin',
    help="""
Your buildout will have a single user, with manager privileges, defined
at the root. This option lets you select the name for this user.
"""
    )

VAR_ZOPE_PASSWD = StringVar(
    'zope_password',
    title='Initial User Password',
    description='Password for Zope root admin user',
    modes=(EXPERT),
    page='Main',
    default='admin',
    help="""
Your buildout will have a single user, "%(zope_user)s", with manager
privileges, defined at the root. This option lets you select the initial
password for this user. If left blank, the password will be randomly
generated.
"""
    )

VAR_HTTP = BoundedIntVar(
    'http_port',
    title='HTTP Port',
    description='Port that Zope will use for serving HTTP',
    default='8080',
    modes=(EXPERT,EASY),
    page='Main',
    help="""
This options lets you select the port # that Zope will use for serving
HTTP.
""",
    min=1024,
    max=65535,
    )
#----------------------------------------------------------------------------------------


class AbstractBuildout(BaseTemplate):
    """Abstract class for all templates that produce buildouts."""

    category = "Buildout"

    vars = copy.deepcopy(BaseTemplate.vars)

