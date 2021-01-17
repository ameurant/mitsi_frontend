# -*- coding: utf-8 -*-
from plone import api


def post_handler(context):
    _add_groups(context)
    _createAllFolders(context)


def _createAllFolders(context):
    portal = api.portal.get()
    # createFolder(parentFolder=portal, folderId='labos', folderTitle='laboratoire', folderLayout='displayBox'):
    # createFolder(parentFolder=portal['labos'], folderId='labos', folderTitle='laboratoire', folderLayout='displayBox'):


def _add_groups(context):
    if not api.group.get('drivers'):
        api.group.create(groupname='drivers', title="Drivers")


def createFolder(parentFolder, folderId, folderTitle, folderLayout=''):
    if folderId not in parentFolder.objectIds():
        newFolder = plone.api.content.create(container=parentFolder, 
                                             type='Folder', 
                                             id=folderId, 
                                             title=folderTitle, 
                                             safe_id=False)
        newFolder.setlayout(folderLayout)

    publishObject(newFolder)  # voir avec api https://docs.plone.org/develop/plone.api/docs/content.html#get-workflow-state
    newFolder.reindexObject()
    return newFolder
