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
        tablesDrivers = self.getLabDbAccess('mitsibox_drivers')
        recs = tablesDrivers.find().execute()
        # recs = tbl_mitsibox.select().execute()
        myDrivers = recs.fetch_all()

        return myDrivers

    def getDriverById(self, idDriver):
        """
        Récupères les infos d'un chauffeur selon son ID
        """
        tablesDrivers = self.getLabDbAccess('mitsibox_drivers')
        recs = tablesDrivers.find("_id=='%s'" % (idDriver,)).execute()
        myDriver = recs.fetch_one()

        return myDriver

    def insertDriver(self):
        """
        insertion d'une nouvelle drivers
        """
        tablesDrivers = self.getLabDbAccess('mitsibox_drivers')
        
        fields = self.request.form

        newDriver = {}
        newDriver['lastName'] = fields.get('driverLastName', None).decode('utf-8')
        newDriver['firstName'] = fields.get('driverFirstName', None).decode('utf-8')
        newDriver['gsm'] = fields.get('driverGsm', None)

        tablesDrivers.add(newDriver).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le chauffeur est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-chauffeurs/listing-des-chauffeurs" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateDriver(self):
        """
        insertion d'une nouvelle boite
        """
        tablesDrivers = self.getLabDbAccess('mitsibox_drivers')
        
        fields = self.request.form
        idDriver = fields.get('idDriver', None)

        myDriver = {}
        myDriver['lastName'] = fields.get('driverLastName', None).decode('utf-8')
        myDriver['firstName'] = fields.get('driverFirstName', None).decode('utf-8')
        myDriver['gsm'] = fields.get('driverGsm', None)

        tablesDrivers.modify("_id='%s'" % idDriver).patch(myDriver).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"les données du chauffeur ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-chauffeurs/listing-des-chauffeurs" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
