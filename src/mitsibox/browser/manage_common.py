# -*- coding: utf-8 -*-

import time
import calendar
from datetime import date, datetime
from Products.Five import BrowserView
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from interfaces import IManageCommon


class ManageCommon(BrowserView):
    implements(IManageCommon)

    def getTimeStamp(self):
        """
        retourne le timestamp courant
        """
        timeStamp = datetime.now()
        return timeStamp

    def getMonth(self):
        """
        retourne une liste de mois
        """
        listeMois = [calendar.month_name[m] for m in range(1, 13)]
        return listeMois

    def getCurrentDate(self):
        """
        retourne la date courante
        """
        currentDate = datetime.now().strftime('%Y-%m-%d')
        return currentDate

    def convertDate(self, dateStr, format="%d/%m/%Y"):
        """
        retourne une date objet selon un format de string reçu
        """
        timeObj = time.strptime(dateStr, format)
        dateObj = date(*timeObj[0:3])
        return dateObj

    def getUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self, 'portal_membership')
        user = pm.getAuthenticatedMember()
        user = user.getUserName()
        return user

    def getRoleUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self.context, 'portal_membership')
        user = pm.getAuthenticatedMember()
        userRole = user.getRoles()
        return userRole
