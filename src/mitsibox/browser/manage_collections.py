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
    gestion des collectes de saclots de prélèvements
    pa' l' tchauffeu.
    """
    implements(IManageCollections)

    def getAllCollections(self):
        """
        Récupères les collectes de saclots
        """
        tableCollections = self.getLabDbAccess('mitsibox_collection')
        recs = tableCollections.find().execute()
        # recs = tbl_mitsibox.select().execute()
        myCollections = recs.fetch_all()
        return myCollections

    def getCollectionById(self, idCollection):
        """
        Récupères les infos d'une collecte de saclot selon son ID
        """
        tableCollections = self.getLabDbAccess('mitsibox_collection')
        recs = tableCollections.find("_id=='%s'" % (idCollection,)).execute()
        myCollection = recs.fetch_one()
        return myCollection

    def insertCollection(self):
        """
        insertion d'une collecte de saclot pa' l'tchauffeu
        """
        tableCollections = self.getLabDbAccessTable('mitsibox_collection')

        fields = self.request.form

        round_id = fields.get('idRound', None)
        driver_id = fields.get('idDriver', None)
        box_id = fields.get('boxId', None)
        total_samples = fields.get('totalSaclots', None)
        samples = fields.get('samples', None)

        tableCollections.insert(['round_id', 'driver_id', 'box_id', 'total_samples', 'samples']).values(round_id, driver_id, box_id, total_samples, samples).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La collecte est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/collecte-des-boites" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateCollection(self):
        """
        update des données d'une collecte de saclots pa' l' tchauffeu
        """
        tableCollections = self.getLabDbAccess('mitsibox_collection')

        fields = self.request.form
        idCollection = fields.get('idCollection', None)

        myCollection = {}
        myCollection['lastName'] = fields.get('driverLastName', None).decode('utf-8')
        myCollection['firstName'] = fields.get('driverFirstName', None).decode('utf-8')
        myCollection['gsm'] = fields.get('driverGsm', None)

        tableCollections.modify("_id='%s'" % idCollection).patch(myCollection).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"les données de la collecte ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/collecte-des-boites" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
