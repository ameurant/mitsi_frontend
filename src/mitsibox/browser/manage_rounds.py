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
        Récupère les infos de toutes les tournées
        """
        session = self.getConnexion()
        db=session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()

        tbl_mitsiround = db.get_collection('mitsibox_rounds')
        recs = tbl_mitsiround.find().execute()
        myRounds = recs.fetch_all()
        return myRounds

    def getRoundById(self, idRound):
        """
        Récupère les infos d'une tournée selon son _id
        """
        session = self.getConnexion()
        db=session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()

        tbl_mitsiround = db.get_collection('mitsibox_rounds')
        recs = tbl_mitsiround.find("_id=='%s'"%(idRound,)).execute()
        myRound = recs.fetch_one()
        return myRound

    def getRoundsOfBox(self, idBox):
        """
        Récupère le nom dde la tournée à la quelle appartient une box
        """
        session = self.getConnexion()
        db=session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()

        tbl_mitsiround = db.get_collection('mitsibox_rounds')

        myRound = session.sql("""select
                                    doc->>"$.roundName"
                                 from
                                    mitsi_chuhautesenne.mitsibox_rounds
                                 where
                                    "%s" member of (doc->>"$.mitsiboxList")""" % (idBox,))
        import pdb; pdb.set_trace()
        return myRound

    def insertRound(self):
        """
        insertion d'une nouvelle tournée
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        round = db.get_collection('mitsibox_rounds')

        fields = self.request.form

        dico = {}
        dico['roundName'] = fields.get('roundName', None)
        dico['roundType'] = fields.get('roundType', None)
        dico['roundStartTime'] = fields.get('roundStartTime', None)
        dico['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        dico['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)

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
        db = session.get_schema('mitsi_chuhautesenne')
        round = db.get_collection('mitsibox_rounds')

        fields = self.request.form
        idRound = fields.get('idRound', None) 

        dico = {}
        dico['roundName'] = fields.get('roundName', None)
        dico['roundType'] = fields.get('roundType', None)
        dico['roundStartTime'] = fields.get('roundStartTime', None)
        dico['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        dico['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)

        newRound = json.dumps(dico)
        
        round.modify("_id='%s'" % idRound).patch(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Les données de la tounrée ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''




# XXXXXXXX 


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

