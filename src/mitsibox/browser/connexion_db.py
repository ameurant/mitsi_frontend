# -*- coding: utf-8 -*-

import mysqlx
from Products.Five import BrowserView


class ConnexionDb(BrowserView):
    """
    recupère toutes les news et les renvoie en JSON
    """
    
    def getConnexion(self):
        """
        crée une connexion sur la db
        """
        session = mysqlx.get_session({
                    'host': '127.0.0.1', 
                    'port': 44060,
                    'user': 'sensiholdv2',
                    'password': '69AlainAvouluJouer$',
                    'ssl-mode': 'DISABLED'
                })

        return session