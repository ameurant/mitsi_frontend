# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ISensiboxCoreLayer(IDefaultBrowserLayer):
    """
    Layer for all mitisibox developments
    """


class IshowBox(Interface):
    """
    IshowBox
    """

class IManageConnexionDb(Interface):
    """
    IManageConnexionDb
    """

class IManageBox(Interface):
    """
    IManageBox
    """


class IManageDisplayBox(Interface):
    """
    IManageDisplayBox
    """
