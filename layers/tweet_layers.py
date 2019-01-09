# -*- coding: utf-8 -*-

import datetime
from abc import abstractmethod
from qgis.core import QgsVectorLayer, QgsField, QgsGeometry, QgsFeature, \
                      QgsCoordinateReferenceSystem, QgsPointXY, QgsRectangle
from PyQt5.QtCore import QVariant



class TweetLayer(QgsVectorLayer):
    """QGIS Layer class wrapper"""
    def __init__(self, proj, name):
        super().__init__("Point?crs={0}".format(proj), ''.join(name), "memory")
        self.proj = proj
        self.pr = self.dataProvider()
        self.feat = None
        self.pr.addAttributes([
            QgsField("status_id", QVariant.String),
            QgsField("user_name", QVariant.String),
            QgsField("localization", QVariant.String),
            QgsField("place", QVariant.String),
            QgsField("tweet", QVariant.String),
            QgsField("time", QVariant.String)
        ])

    @abstractmethod    
    def add_tweet_feature(self, tweet):
        self.feat = QgsFeature()
    
    @staticmethod
    def format_tweet_date(tweet_date):
        tweet_time = datetime.datetime.utcfromtimestamp(
            float("{0}.{1}".format(tweet_date[:-3], tweet_date[11:13]))
            ).strftime('%Y-%m-%d %H:%M:%S:%f')
        return tweet_time
    
    @staticmethod
    def create_place_rect(tweet_place):
        rect = QgsRectangle(
            tweet_place.bounding_box.coordinates[0][0][0],
            tweet_place.bounding_box.coordinates[0][0][1],
            tweet_place.bounding_box.coordinates[0][2][0],
            tweet_place.bounding_box.coordinates[0][2][1]
            )
    
    def highlight_tweet_feature(self, tweet, iface):
        feat_iter = self.getFeatures(' "status_id" is {0} '.format(tweet['status_id']))
        crs = QgsCoordinateReferenceSystem(self.proj)
        for feat in feat_iter:
            iface.mapCanvas().flashGeometries([feat.geometry()], crs, flashes=5, duration=800)


class GeoTweetLayer(TweetLayer):
    """subclass for geo-located tweets"""
    def __init__(self, proj, name):
        self.src_type = "_geo_tweets"
        name = "{0}{1}".format(name, self.src_type)
        super().__init__(proj, name)
    
    def add_tweet_feature(self, tweet):
        super().add_tweet_feature(tweet)
        tweet_time = self.format_tweet_date(tweet['time'])
        self.feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(tweet['geo']['coordinates'][1], tweet['geo']['coordinates'][0])))
        if tweet['place'] is not None:
            self.feat.setAttributes([
            tweet['status_id'],
            tweet['user'],
            tweet['localization'],
            "{0}, {1}".format(tweet['place'].full_name, tweet['place'].country),
            tweet['tweet'],
            tweet_time
            ])
        else:
            self.feat.setAttributes([
                tweet['status_id'],
                tweet['user'],
                tweet['localization'],
                "no place given",
                tweet['tweet'],
                tweet_time
            ])
        self.pr.addFeatures([self.feat])
        self.commitChanges()
        self.triggerRepaint()
        self.updateFields()


class PlaceTweetLayer(TweetLayer):
    """subclass for place-located tweets"""
    def __init__(self, proj, name):
        self.src_type = "_place_tweets"
        name = "{0}{1}".format(name, self.src_type)
        super().__init__(proj, name)
        self.rect = None
    
    def add_tweet_feature(self, tweet):
        super().add_tweet_feature(tweet)
        tweet_time = self.format_tweet_date(tweet['time'])
        # we only grab tweets having a coordinates
        try: 
            if tweet['place'].bounding_box.coordinates[0][1][0] is not None:
                self.rect = self.create_place_rect(tweet['place'])
                print("tweet at location {0} found".format(str(tweet['place'].bounding_box.coordinates[0][1][0])))
                self.feat.setGeometry(QgsGeometry.fromPointXY(
                    QgsPointXY(tweet['place'].bounding_box.coordinates[0][1][0],
                            tweet['place'].bounding_box.coordinates[0][1][1])))
                self.feat.setAttributes([
                        tweet['status_id'],
                        tweet['user'],
                        tweet['localization'],
                        "{0}, {1}".format(tweet['place'].full_name, tweet['place'].country),
                        tweet['tweet'],
                        tweet_time
                    ])
            self.pr.addFeatures([self.feat])
            self.commitChanges()
            self.triggerRepaint()
            self.updateFields()
        except TypeError as e:
            print("Exception {0}, for tweet {1}".format(e.message, tweet['status_id']))