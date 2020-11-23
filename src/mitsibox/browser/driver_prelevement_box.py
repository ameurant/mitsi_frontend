# -*- coding: utf-8 -*-

import json
# import mysqlx
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from interfaces import IManageDriverPrelevementBox
from connexion_db import ConnexionDb


class DriverPrelevementBox(ConnexionDb):
    """
    recupère toutes infos collectées par un chauffeur
    lors de sa tournée
    """
    implements(IManageDriverPrelevementBox)

    