# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageCollections
from connexion_db import ConnexionDb


class ManageCollections(ConnexionDb):
    """
    gestion des collecte des saclots lors d'une tournéee
    """
    implements(IManageCollections)


    def insertCollection(self):
        """
        insertion d'une nouvelle collecte par un driver
        """
        tableCollectionss = self.getLabDbAccess('mitsibox_collection')
        fields = self.request.form

        newCollection = {}
        newCollection['roundName'] = fields.get('roundName', None).decode("utf-8")
        newCollection['roundType'] = fields.get('roundType', None)
        newCollection['roundStartTime'] = fields.get('roundStartTime', None)
        newCollection['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        newCollection['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)
        newCollection['roundDriverId'] = fields.get('roundDriverId', None)

        tableCollections.add(newCollection).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La collection est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/collecte-des-boites" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateCollection(self):
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
        newRound['roundDriverId'] = fields.get('roundDriverId', None)

        tablesRounds.modify("_id='%s'" % idRound).patch(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Les données de la tounrée ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-tournees/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
