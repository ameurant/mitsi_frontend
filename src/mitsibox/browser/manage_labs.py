# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageLabs
from connexion_db import ConnexionDb


class ManageLabs(ConnexionDb):
    """
    gestion des laboratoires
    """
    implements(IManageLabs)

    def getListingLabs(self):
        """
        Récupères les infos de toutes les labos
        """
        session = self.getConnexion()
        db = session.get_schema('mitsibox')
        labs = db.get_collection('mitsibox_labs')

        recs = labs.find().execute()
        #recs = tbl_mitsibox.select().execute()
        allLabs = recs.fetch_all()
        return allLabs


    def insertLabs(self):
        """
        insertion d'un nouveau laboratoire
        """
        session = self.getConnexion()
        db=session.get_schema('mitsibox')
        labs = db.get_collection('mitsibox_labs')

        fields = self.request.form

        dico={}
        dico['name'] = fields.get('labsName', None)
        dico['address'] = fields.get('labsAddress', None)
        dico['cp'] = fields.get('labsCp', None)
        dico['localite'] = fields.get('labsLocalite', None)
        dico['lat'] = fields.get('labsLat', None)
        dico['long'] = fields.get('labsLong', None)
        
        newLabs = json.dumps(dico)

        labs.add(newLabs).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok le nouveau laboratoire est créé."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-labs" % (portalUrl,)
        self.request.response.redirect(url)
        return ''


    def updateLabs(self):
        """
        modification des données d'un laboratoire
        """
        session = self.getConnexion()
        db=session.get_schema('mitsibox')
        labs = db.get_collection('mitsibox_labs')

        fields = self.request.form

        dico={}
        dico['name'] = fields.get('labsName', None)
        dico['address'] = fields.get('labsAddress', None)
        dico['cp'] = fields.get('labsCp', None)
        dico['localite'] = fields.get('labsLocalite', None)
        dico['lat'] = fields.get('labsLat', None)
        dico['long'] = fields.get('labsLong', None)
        
        newLabs = json.dumps(dico)

        #box.modify("_id='%s'" % box_id).patch(patch_json).execute()(newBoite).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok Les données du laboratoire ont été modifiées"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/listing-labs" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

