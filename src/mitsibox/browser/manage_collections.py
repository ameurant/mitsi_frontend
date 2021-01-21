# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageCollections
from connexion_db import ConnexionDb
import mysql.connector


class ManageCollections(ConnexionDb):
    """
    gestion des collectes de saclots de prélèvements
    pa' l' tchauffeu.
    """
    implements(IManageCollections)

    def getAllCollections(self):
        """
        Récupères les collectes de saclots 
        table mitsibox_collect_history
        """
        tableCollections = self.getLabDbAccessTable('mitsibox_collect_history')
        recs = tableCollections.select().execute()  # cas d'une table
        myCollections = recs.fetch_all()
        return myCollections

    def getCollectionById(self, idCollection):
        """
        Récupère les infos d'une collecte de saclot selon son ID
        table mitsibox_collect_history
        """
        tableCollections = self.getLabDbAccessTable('mitsibox_collect_history')
        recs = tableCollections.find("_id=='%s'" % (idCollection,)).execute()
        myCollection = recs.fetch_one()
        return myCollection

    def insertCollection(self):
        """
        insertion d'une collecte de saclot pa' l'tchauffeu
        table mitsibox_collect_history
        """
        fields = self.request.form
        round_id = fields.get('idRound', None)
        driver_id = fields.get('idDriver', None)
        samples_total = fields.get('totalSaclots', None)
        collect_comment = fields.get('collectComment', None)
        box_id = fields.get('boxId', None)
        collect_box_comment = fields.get('collectBoxComment', None)
        status = 'ACTIVE'

        # ouverture de la connexion
        session = self.getConnexion()
        db = session.get_schema("mitsi_chuhautesenne")

        # recupe des deux tables
        tableCollectHistory = db.get_table('mitsibox_collect_history')
        tableCollectBoxHistory = db.get_table('mitsibox_collect_box_history')

        # Insertion dans la table tableCollectHistory
        # tableCollectHistory = self.getLabDbAccessTable('mitsibox_collect_history')
        tableCollectHistory.insert(['round_id', 'driver_id', 'box_id', 'samples_total', 'collect_comment', 'status']).values(round_id, driver_id, box_id, samples_total, collect_comment, status).execute()
        session.commit()

        # recup du dernier _id qui vient d'être inséré
        request = session.sql("select last_insert_id()").execute()
        collect_history_id = request.fetch_one()[0]
        print "collect_history_id : %s" % (collect_history_id,)
        print "box_id : %s" % (box_id,)

        # Insertion dans la table tableCollectBoxHistory
        # tableCollectBoxHistory = self.getLabDbAccessTable('mitsibox_collect_box_history')
        tableCollectBoxHistory.insert(['collect_history_id', 'box_id', 'collect_box_comment']).values(collect_history_id, box_id, collect_box_comment).execute()
        session.commit()

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
        table mitsibox_collect_history
        """
        tableCollections = self.getLabDbAccessTable('mitsibox_collect_history')

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
