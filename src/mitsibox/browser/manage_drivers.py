# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageDrivers
from connexion_db import ConnexionDb


class ManageDrivers(ConnexionDb):
    """
    gestion des boites
    """
    implements(IManageDrivers)

    def getAllDrivers(self):
        """
        Récupères les infos de toutes les chauffeurs
        """
        session = self.getConnexion()

        db=session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()
        
        tbl_mitsidriver = db.get_collection('mitsibox_drivers')
        recs = tbl_mitsidriver.find().execute()
        #recs = tbl_mitsibox.select().execute()
        myDrivers = recs.fetch_all()
        
        return myDrivers

    def insertDriver(self):
        """
        insertion d'une nouvelle drivers
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        box = db.get_collection('mitsibox_drivers')

        fields = self.request.form

        dico = {}
        dico['lastName'] = fields.get('driverLastName', None)
        dico['firstName'] = fields.get('driverFirstName', None)
        dico['gsm'] = fields.get('driverGsm', None)
        
        newDriver = json.dumps(dico)

        box.add(newDriver).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le chauffeur est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-des-chauffeurs" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateDriver(self):
        """
        insertion d'une nouvelle boite
        """
        session = self.getConnexion()
        db = session.get_schema('mitsibox')
        box = db.get_collection('mitsibox_drivers')

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
