# -*- coding: utf-8 -*-

import mysqlx
from Products.Five import BrowserView


class ConnexionDb(BrowserView):
    """
    connexion sur la db mitsibox
    """

    def getConnexion(self):
        """
        crée une connexion sur la db
        """
        session = mysqlx.get_session({
                    'host': '127.0.0.1', 
                    'port': 33060,
                    'user': 'mitsibox',
                    'password': '69AlainAvouluJouer$',
                    'ssl-mode': 'DISABLED'
                })

        return session
