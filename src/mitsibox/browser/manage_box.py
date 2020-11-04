# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageBox
from connexion_db import ConnexionDb


class ManageBox(ConnexionDb):
    """
    gestion des boites
    """
    implements(IManageBox)

    def getListingBox(self):
        """
        Récupères les infos de toutes les boites
        """
        session = self.getConnexion()

        db = session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()

        tbl_mitsibox = db.get_collection('mitsibox_boxes')
        recs = tbl_mitsibox.find().execute()
        # recs = tbl_mitsibox.select().execute()
        myBoxes = recs.fetch_all()

        return myBoxes

    def getOneBoxById(self, idBox):
        """
        Récupères les infos d'une boite selon son identifiant
        """
        session = self.getConnexion()

        db = session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()

        tbl_mitsibox = db.get_collection('mitsibox_boxes')
        recs = tbl_mitsibox.find("_id=='%s'"%(idBox,)).execute()
        myBoxe = recs.fetch_one()

        return myBoxe

    def insertBox(self):
        """
        insertion d'une nouvelle boite
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        box = db.get_collection('mitsibox_boxes')

        fields = self.request.form

        newBox = {}
        newBox['lab_id'] = fields.get('laboId', None)
        newBox['name'] = fields.get('boxName', None)
        newBox['address'] = fields.get('boxAddress', None)
        newBox['cp'] = fields.get('boxCp', None)
        newBox['localite'] = fields.get('boxLocalite', None)
        newBox['lat'] = fields.get('boxLat', None)
        newBox['long'] = fields.get('boxLong', None)
        newBox['ssid'] = fields.get('boxSsidWifi', None)
        newBox['passwifi'] = fields.get('boxPassWifi', None)
        newBox['arduino'] = fields.get('boxArduino', None)

        box.add(newBox).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok les données de la boite ont été enregistrées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-boites/listing-des-mitsibox" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateBox(self):
        """
        insertion d'une nouvelle boite
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        box = db.get_collection('mitsibox_boxes')

        fields = self.request.form
        idBox = fields.get('idBox', None)

        myBox = {}
        myBox['lab_id'] = fields.get('laboId', None)
        myBox['name'] = fields.get('boxName', None).decode("utf-8")
        myBox['address'] = fields.get('boxAddress', None).decode("utf-8")
        myBox['cp'] = fields.get('boxCp', None)
        myBox['localite'] = fields.get('boxLocalite', None).decode("utf-8")
        myBox['lat'] = fields.get('boxLat', None)
        myBox['long'] = fields.get('boxLong', None)
        myBox['ssid'] = fields.get('boxSsidWifi', None)
        myBox['passwifi'] = fields.get('boxPassWifi', None)
        myBox['arduino'] = fields.get('boxArduino', None)

        box.modify("_id='%s'" % idBox).patch(myBox).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok les données de cette boite ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-boites/listing-des-mitsibox" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
