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

        db=session.get_schema('mitsi_chuhautesenne')
        tables = db.get_tables()
        
        tbl_mitsibox = db.get_collection('mitsibox_boxes')
        recs = tbl_mitsibox.find().execute()
        #recs = tbl_mitsibox.select().execute()
        myBoxes = recs.fetch_all()
        
        return myBoxes

    def getOneBoxById(self, idBox):
        """
        Récupères les infos d'une boite selon son identifiant
        """
        session = self.getConnexion()

        db=session.get_schema('mitsi_chuhautesenne')
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

        dico = {}
        dico['lab_id'] = fields.get('laboId', None)
        dico['name'] = fields.get('boxName', None)
        dico['address'] = fields.get('boxAddress', None)
        dico['cp'] = fields.get('boxCp', None)
        dico['localite'] = fields.get('boxLocalite', None)
        dico['lat'] = fields.get('boxLat', None)
        dico['long'] = fields.get('boxLong', None)
        dico['ssid'] = fields.get('boxSsidWifi', None)
        dico['passwifi'] = fields.get('boxPassWifi', None)

        newBoite = json.dumps(dico)

        box.add(newBoite).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok le guide a été bien enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-des-mitsibox" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateBox(self):
        """
        insertion d'une nouvelle boite
        """
        session = self.getConnexion()
        db = session.get_schema('mitsibox')
        box = db.get_collection('mitsibox_boxes')

        fields = self.request.form

        dico = {}
        dico['lab_id'] = fields.get('laboId', None)
        dico['name'] = fields.get('boxName', None)
        dico['address'] = fields.get('boxAddress', None)
        dico['cp'] = fields.get('boxCp', None)
        dico['localite'] = fields.get('boxLocalite', None)
        dico['lat'] = fields.get('boxLat', None)
        dico['long'] = fields.get('boxLong', None)
        dico['ssid'] = fields.get('boxSsidWifi', None)
        dico['passwifi'] = fields.get('boxPassWifi', None)

        newBoite = json.dumps(dico)

        # box.modify("_id='%s'" % box_id).patch(patch_json).execute()(newBoite).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok le guide a été bien enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-des-mitsibox" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
