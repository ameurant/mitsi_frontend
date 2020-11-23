# -*- coding: utf-8 -*-

import mysqlx
from Products.Five import BrowserView

LABNAME = "mitsi_chuhautesenne"

class ConnexionDb(BrowserView):
    """
    connexion sur la db mitsibox
    """

    def getConnexion(self):
        """
        crée une connexion sur la db
        en local 44060
        sur becker 33060
        """
        session = mysqlx.get_session({
                    'host': '127.0.0.1', 
                    'port': 33060,
                    'user': 'mitsibox',
                    'password': '69AlainAvouluJouer$',
                    'ssl-mode': 'DISABLED'
                })

        return session

    def getLabDbAccess(self, tableName):
        """
        recupère les tables d'un laboratoire
        """
        session = self.getConnexion()
        db = session.get_schema(LABNAME)
        tablesMitsibox = db.get_collection(tableName)
        return tablesMitsibox
