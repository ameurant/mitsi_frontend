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
        tablesRounds = self.getLabDbAccess('mitsibox_rounds')
        recs = tablesRounds.find().execute()
        myRounds = recs.fetch_all()
        return myRounds

    def getRoundById(self, idRound):
        """
        Récupère les infos d'une tournée selon son _id
        """
        tablesRounds = self.getLabDbAccess('mitsibox_rounds')
        recs = tablesRounds.find("_id =='%s'"%(idRound,)).execute()
        myRound = recs.fetch_one()
        return myRound

    def getRoundsOfBox(self, idBox):
        """
        Récupère le nom dde la tournée à la quelle appartient une box
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        request = db.session.sql("""select
                                        doc->>"$._id",
                                        doc->>"$.roundName"
                                    from
                                        mitsi_chuhautesenne.mitsibox_rounds
                                    where
                                        "%s" member of (doc->>'$.roundMitsiboxList')""" % (idBox,)).execute() 
        myRound = {}
        (myRound['idRound'], myRound['roundName']) = request.fetch_one()
        return myRound

    def getDistanceRound(self, idRound):
        """
        Calcule la distance d'une tournée
        """
        session = self.getConnexion()
        request = session.sql("select sum(dist) 'round distance' from (select ST_Distance(geo_point, lag(geo_point) OVER w, 'kilometre') as 'dist'  from mitsi_chuhautesenne.mitsibox_boxes where _id IN ('{}') window w as (ORDER BY FIELD(_id,'{}'))) as t".format("','".join('mitsi_chuhautesenne'.mitsibox_rounds.find("_id='00005ecb95df000000000000001d'").fields("box_list").execute().fetch_one()['box_list']),"','".join('mitsi_chuhautesenne'.mitsibox_rounds.find("_id='00005ecb95df000000000000001d'").fields("box_list").execute().fetch_one()['box_list'])))

        myDistance = request.fetch_one()[0]
        return myDistance

    def insertRound(self):
        """
        insertion d'une nouvelle tournée
        """
        tableRounds = self.getLabDbAccess('mitsibox_rounds')
        fields = self.request.form

        newRound = {}
        newRound['roundName'] = fields.get('roundName', None).decode("utf-8")
        newRound['roundType'] = fields.get('roundType', None)
        newRound['roundStartTime'] = fields.get('roundStartTime', None)
        newRound['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        newRound['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)

        tableRounds.add(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La tounrée est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-tournees/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateRound(self):
        """
        modification d'une tournée
        """
        tablesRounds = self.getLabDbAccess('mitsibox_rounds')
        fields = self.request.form
        idRound = fields.get('idRound', None) 

        newRound = {}
        newRound['roundName'] = fields.get('roundName', None).decode("utf-8")
        newRound['roundType'] = fields.get('roundType', None)
        newRound['roundStartTime'] = fields.get('roundStartTime', None)
        newRound['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        newRound['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)

        tablesRounds.modify("_id='%s'" % idRound).patch(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Les données de la tounrée ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-tournees/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
