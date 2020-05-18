# -*- coding: utf-8 -*-

import json
#import mysqlx
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from interfaces import IManageDisplayBox
from connexion_db import ConnexionDb

class DisplayBox(ConnexionDb):
    """
    recupère toutes les news et les renvoie en JSON
    """
    implements(IManageDisplayBox)
    
    def getJsonBox(self):
        """
        récupère les paramètres des boites au format JSON
        """
        session = self.getConnexion()
        db=session.get_schema('mitsibox')
        tables = db.get_tables()
        
        tbl_mitsibox = db.get_collection('mitsibox_boxes')
        recs = tbl_mitsibox.find().execute()
        myBoxes = recs.fetch_all()
        
        idList=[]
        for el in recs.fetch_all():
            idList.append(dict(el))
        boites = json.dumps(idList)
        return boites


    def getListingBox(self):
        """
        Récupères les infos de toutes les boites
        """
        session = self.getConnexion()

        db=session.get_schema('mitsibox')
        tables = db.get_tables()
        
        tbl_mitsibox = db.get_collection('mitsibox_boxes')
        recs = tbl_mitsibox.find().execute()
        #recs = tbl_mitsibox.select().execute()
        myBoxes = recs.fetch_all()
        
        return myBoxes

    def getOneBox(self, idBox):
        """
        Récupères les infos d'une boite selon son tidentifiant
        """

        session = self.getConnexion()

        db=session.get_schema('mitsibox')
        tables = db.get_tables()
        
        tbl_mitsibox = db.get_collection('mitsibox_boxes')
        recs = tbl_mitsibox.find("_id=='%s'"%(idBox,)).execute()
        myBoxe = recs.fetch_one()
        
        return myBoxe

        #box=col.find("_id=idBox").execute()
