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
    
    def insertBox(self):
        """
        insertion d'une nouvelle boite
        """
        session = self.getConnexion()
        db=session.get_schema('mitsibox')
        box = db.get_collection('mitsibox_boxes')

        fields = self.request.form

        dico={}
        dico['lab_id'] = fields.get('laboId', None)
        dico['name'] = fields.get('boxName', None)
        dico['address'] = fields.get('boxAddress', None)
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
        url = "%s/listing-box" % (portalUrl,)
        self.request.response.redirect(url)
        return ''


    def updateBox(self):
        """
        insertion d'une nouvelle boite
        """
        session = self.getConnexion()
        db=session.get_schema('mitsibox')
        box = db.get_collection('mitsibox_boxes')

        fields = self.request.form

        dico={}
        dico['lab_id'] = fields.get('laboId', None)
        dico['name'] = fields.get('boxName', None)
        dico['address'] = fields.get('boxAddress', None)
        dico['lat'] = fields.get('boxLat', None)
        dico['long'] = fields.get('boxLong', None)
        dico['ssid'] = fields.get('boxSsidWifi', None)
        dico['passwifi'] = fields.get('boxPassWifi', None)
        
        newBoite = json.dumps(dico)
        
        #box.modify("_id='%s'" % box_id).patch(patch_json).execute()(newBoite).execute()
        

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok le guide a été bien enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-box" % (portalUrl,)
        self.request.response.redirect(url)
        return ''




    




