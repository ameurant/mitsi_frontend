# -*- coding: utf-8 -*-

from plone import api
from Products.Five import BrowserView


class DossierImageView(BrowserView):
    """
    Lister les dossiers par bloc avec une image comme prorpriété du dossier
    """

    @property
    def getDossierImage(self):
        """
        selection des dossiers locaux
        triès selon leur position
        récupération de l'image prpriété du dossier
        """
        brains = api.content.find(
                    context=self.context,
                    depth=1,
                    sort_on='getObjPositionInParent',
                    portal_type='Folder',
                 )

        if not brains:
            return None
        dossiers = []
        for b in brains:
            obj = b.getObject()
            dossier = {
                'title': b.Title,
                'description': b.Description,
                'image': obj.image,
                'url': b.getURL(),
            }
            dossiers.append(dossier)
        return dossiers
