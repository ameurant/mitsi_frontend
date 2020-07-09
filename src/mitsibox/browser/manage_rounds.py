# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageRounds
from connexion_db import ConnexionDb


class ManageRounds(ConnexionDb):
    """
    gestion des tournées
    """
    implements(IManageRounds)

    def getAllRounds(self):
        """
        Récupères les infos de toutes les tournées
        """
        session = self.getConnexion()

        db=session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()
        
        tbl_mitsidriver = db.get_collection('mitsibox_rounds')
        recs = tbl_mitsidriver.find().execute()
        #recs = tbl_mitsibox.select().execute()
        myRounds = recs.fetch_all()
        
        return myRounds

    def insertRound(self):
        """
        insertion d'une nouvelle tournée
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        round = db.get_collection('mitsibox_rounds')

        fields = self.request.form


# XXXXXXXX 
#    UTILISER LE CODE DE FRED POUR AJOUTER UN ENSEMBLE
#    D'ID DE BOITES DANS UN ROUND

# Ajouter
# driver_id=db.mitsibox_drivers.find("firstname='Steve'").fields('_id')
# box_list=db.mitsibox_boxes.find().fields('_id')
# box_list_arr=[]
# for el in box_list.execute().fetch_all():
#    box_list_arr.append(el.values()[0])
# doc={"name": "du chef", "type": "daily", "box_list": box_list_arr, "start_time": "09:00:00", "estimated_end_time": "17:00:00"}
# db.mitsibox_rounds.add(doc)


# Lister
# db.mitsibox_rounds.find()
# {
#     "_id": "00005ecb95df0000000000000016",
#     "name": "du chef",
#     "type": "daily",
#     "box_list": [
#         "00005ecb95df000000000000000c",
#         "00005ecb95df0000000000000010",
#         "00005ecb95df0000000000000011",
#         "00005ecb95df0000000000000012"
#     ],
#     "start_time": "09:00:00",
#     "estimated_end_time": "17:00:00"
# }


        dico = {}
        dico['roundtName'] = fields.get('roundtName', None)
        dico['mitsiboxList'] = fields.get('mitsiboxList', None)

        newRound = json.dumps(dico)

        round.add(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La tounrée est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateRound(self):
        """
        modification d'une tournée
        """
        session = self.getConnexion()
        db = session.get_schema('mitsibox')
        box = db.get_collection('mitsibox_rounds')

        fields = self.request.form

        dico = {}
        dico['nom'] = fields.get('driverNom', None)
        dico['prenom'] = fields.get('driverPrenom', None)
        dico['gsm'] = fields.get('driverGsm', None)

        newDriver = json.dumps(dico)

        # box.modify("_id='%s'" % box_id).patch(patch_json).execute()(newBoite).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"les données du chauffeur ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-des-chauffeurs" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
