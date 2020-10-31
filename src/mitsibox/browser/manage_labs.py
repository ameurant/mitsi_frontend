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

    def getLabsById(self, idLab):
        """
        Récupères les infos d'un labo selon son ID
        """
        session = self.getConnexion()
        db = session.get_schema('mitsibox')
        labs = db.get_collection('mitsibox_labs')

        recs = labs.find("_id=='%s'"%(idLab,)).execute()
        myLab = recs.fetch_one()
        
        return myLab

    def createSchemaLab(self, schemaDB):
        """
        creation du schema, des collections des tables
        collection: mitsibox_boxes
        4 tables relationnelles
        mitsibox_frontdoor_events, mitsibox_humidity_events, 
        mitsibox_temperature_events, mitsibox_top_events
        """
        session = self.getConnexion()
        session.create_schema(schemaDB)
        session.sql("""CREATE TABLE {}.`mitsibox_frontdoor_events` (
                          `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                          `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                          `box_id` varbinary(32) DEFAULT NULL,
                          `value` varchar(10) DEFAULT NULL,
                          PRIMARY KEY (`id`,`time_stamp`),
                          KEY `box_id_idx` (`box_id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            /*!50100 PARTITION BY RANGE (unix_timestamp(`time_stamp`))
                            (PARTITION p0 VALUES LESS THAN (1585692000) ENGINE = InnoDB,
                             PARTITION p1 VALUES LESS THAN (1588284000) ENGINE = InnoDB,
                             PARTITION p2 VALUES LESS THAN (1590962400) ENGINE = InnoDB,
                             PARTITION p3 VALUES LESS THAN (1593554400) ENGINE = InnoDB,
                             PARTITION p4 VALUES LESS THAN (1596232800) ENGINE = InnoDB,
                             PARTITION p5 VALUES LESS THAN (1598911200) ENGINE = InnoDB,
                             PARTITION p6 VALUES LESS THAN (1601503200) ENGINE = InnoDB,
                             PARTITION p7 VALUES LESS THAN (1604185200) ENGINE = InnoDB,
                             PARTITION p8 VALUES LESS THAN (1606777200) ENGINE = InnoDB,
                             PARTITION p9 VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */""".format(schemaDB)).execute()
        
        session.sql("""CREATE TABLE {}.`mitsibox_humidity_events` (
                          `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                          `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                          `box_id` varbinary(32) DEFAULT NULL,
                          `value` decimal(5,2) DEFAULT NULL,
                          PRIMARY KEY (`id`,`time_stamp`),
                          KEY `box_id_idx` (`box_id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                        /*!50100 PARTITION BY RANGE (unix_timestamp(`time_stamp`))
                        (PARTITION p0 VALUES LESS THAN (1585692000) ENGINE = InnoDB,
                         PARTITION p1 VALUES LESS THAN (1588284000) ENGINE = InnoDB,
                         PARTITION p2 VALUES LESS THAN (1590962400) ENGINE = InnoDB,
                         PARTITION p3 VALUES LESS THAN (1593554400) ENGINE = InnoDB,
                         PARTITION p4 VALUES LESS THAN (1596232800) ENGINE = InnoDB,
                         PARTITION p5 VALUES LESS THAN (1598911200) ENGINE = InnoDB,
                         PARTITION p6 VALUES LESS THAN (1601503200) ENGINE = InnoDB,
                         PARTITION p7 VALUES LESS THAN (1604185200) ENGINE = InnoDB,
                         PARTITION p8 VALUES LESS THAN (1606777200) ENGINE = InnoDB,
                         PARTITION p9 VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */""".format(schemaDB)).execute()

        session.sql("""CREATE TABLE {}.`mitsibox_temperature_events` (
                          `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                          `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                          `box_id` varbinary(32) DEFAULT NULL,
                          `value` decimal(5,2) DEFAULT NULL,
                          PRIMARY KEY (`id`,`time_stamp`),
                          KEY `box_id_idx` (`box_id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                        /*!50100 PARTITION BY RANGE (unix_timestamp(`time_stamp`))
                        (PARTITION p0 VALUES LESS THAN (1585692000) ENGINE = InnoDB,
                         PARTITION p1 VALUES LESS THAN (1588284000) ENGINE = InnoDB,
                         PARTITION p2 VALUES LESS THAN (1590962400) ENGINE = InnoDB,
                         PARTITION p3 VALUES LESS THAN (1593554400) ENGINE = InnoDB,
                         PARTITION p4 VALUES LESS THAN (1596232800) ENGINE = InnoDB,
                         PARTITION p5 VALUES LESS THAN (1598911200) ENGINE = InnoDB,
                         PARTITION p6 VALUES LESS THAN (1601503200) ENGINE = InnoDB,
                         PARTITION p7 VALUES LESS THAN (1604185200) ENGINE = InnoDB,
                         PARTITION p8 VALUES LESS THAN (1606777200) ENGINE = InnoDB,
                         PARTITION p9 VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */""".format(schemaDB)).execute()

        session.sql("""CREATE TABLE {}.`mitsibox_top_events` (
                          `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                          `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                          `box_id` varbinary(32) DEFAULT NULL,
                          `value` varchar(10) DEFAULT NULL,
                          PRIMARY KEY (`id`,`time_stamp`),
                          KEY `box_id_idx` (`box_id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                        /*!50100 PARTITION BY RANGE (unix_timestamp(`time_stamp`))
                        (PARTITION p0 VALUES LESS THAN (1585692000) ENGINE = InnoDB,
                         PARTITION p1 VALUES LESS THAN (1588284000) ENGINE = InnoDB,
                         PARTITION p2 VALUES LESS THAN (1590962400) ENGINE = InnoDB,
                         PARTITION p3 VALUES LESS THAN (1593554400) ENGINE = InnoDB,
                         PARTITION p4 VALUES LESS THAN (1596232800) ENGINE = InnoDB,
                         PARTITION p5 VALUES LESS THAN (1598911200) ENGINE = InnoDB,
                         PARTITION p6 VALUES LESS THAN (1601503200) ENGINE = InnoDB,
                         PARTITION p7 VALUES LESS THAN (1604185200) ENGINE = InnoDB,
                         PARTITION p8 VALUES LESS THAN (1606777200) ENGINE = InnoDB,
                         PARTITION p9 VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */""".format(schemaDB)).execute()

        session.sql("""CREATE TABLE {}.`mitsibox_collect_history` (
                            `id` int unsigned NOT NULL AUTO_INCREMENT,
                            `round_id` varbinary(32) DEFAULT NULL,
                            `driver_id` varbinary(32) DEFAULT NULL, 
                            `start_date` date DEFAULT NULL, 
                            `start_time` time DEFAULT NULL, 
                            `end_time` time DEFAULT NULL, 
                            `status` varchar(15) DEFAULT NULL, 
                            `samples_total` int DEFAULT NULL, 
                            `collect_comment` varchar(255) DEFAULT NULL, 
                            PRIMARY KEY (`id`))""".format(schemaDB)).execute()
        
        session.sql("""CREATE TABLE {}.`mitsibox_collect_box_history` (
                            `id` int unsigned NOT NULL AUTO_INCREMENT,
                            `collect_history_id` int unsigned DEFAULT NULL,
                            `box_id` varbinary(32) DEFAULT NULL,
                            `collect_box_timestamp` timestamp NULL DEFAULT NULL,
                            `collect_box_comment` varchar(255) DEFAULT NULL,
                            PRIMARY KEY (`id`))""".format(schemaDB)).execute()

        session.get_schema(schemaDB).create_collection('mitsibox_boxes')
        session.get_schema(schemaDB).create_collection('mitsibox_drivers')
        session.get_schema(schemaDB).create_collection('mitsibox_rounds')

    def insertLabs(self):
        """
        insertion d'un nouveau laboratoire
        """
        session = self.getConnexion()
        db=session.get_schema('mitsibox')
        labs = db.get_collection('mitsibox_labs')

        fields = self.request.form

        schema = fields.get('labsSchema', None)
        schemaDB = "mitsi_%s" % (schema)

        newLab={}
        newLab['name'] = fields.get('labsName', None).decode('utf-8')
        newLab['address'] = fields.get('labsAddress', None).decode('utf-8')
        newLab['cp'] = fields.get('labsCp', None)
        newLab['localite'] = fields.get('labsLocalite', None).decode('utf-8')
        newLab['lat'] = fields.get('labsLat', None)
        newLab['long'] = fields.get('labsLong', None)
        newLab['schema'] = schemaDB

        labs.add(newLab).execute()

        self.createSchemaLab(schemaDB)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok le nouveau laboratoire est créé."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-laboratoires/listing-des-laboratoires" % (portalUrl,)
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
        idLab = fields.get('idLab', None)

        myLab={}
        myLab['name'] = fields.get('labsName', None).decode('utf-8')
        myLab['address'] = fields.get('labsAddress', None).decode('utf-8')
        myLab['cp'] = fields.get('labsCp', None)
        myLab['localite'] = fields.get('labsLocalite', None).decode('utf-8')
        myLab['lat'] = fields.get('labsLat', None)
        myLab['long'] = fields.get('labsLong', None)

        labs.modify("_id='%s'" % idLab).patch(myLab).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Ok Les données du laboratoire ont été modifiées"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-laboratoires/listing-des-laboratoires" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
