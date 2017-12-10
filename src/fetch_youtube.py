import sys
import string
import csv
import requests
import urllib2
import json
import datetime, dateutil.parser
import numpy as np
import pickle
import pandas as pd
'''
Stats Needed: 
1) SubscriberCount
2) ChannelVideoCount
3) ChannelViewCount
4) PrevCommentCount
5) PrevDislikeCount
6) PrevViewCount
7) Weeks since upload 
8) ChannelAge
'''

key = 'AIzaSyCrFWiPfGcb5IsyS-wpAMk6eaNdMaC8pXs'
vidStats = 'https://www.googleapis.com/youtube/v3/videos?part=id,statistics&id='
vidSnips = 'https://www.googleapis.com/youtube/v3/videos?part=id,snippet&id='
channelStats = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id='
channel = 'UChUEb7Fczc6jyXo-R0qnn8Q'

class YoutTubeFetcher(object):
    def __init__(self, api_key):
        self.apikey = api_key
        self.subscriberCount = 0
        self.channelVideoCount = 0
        self.channelViewCount = 0
        self.prevCommentCount = 0
        self.prevLikeCount = 0
        self.prevDislikeCount = 0
        self.PrevViewCount = 0
        self.ChannelAge = 0

    def get(self, channelID):

        '''
        Channel Stats
        '''

        stats = json.load(urllib2.urlopen(channelStats + channelID + '&key=' + self.apikey))
        self.subscriberCount = stats['items'][0]['statistics']['subscriberCount']
        self.channelVideoCount = stats['items'][0]['statistics']['videoCount']
        self.channelViewCount = stats['items'][0]['statistics']['viewCount']

        self.ChannelAge = stats['items'][0]['snippet']['publishedAt']
        self.ChannelAge = dateutil.parser.parse(self.ChannelAge)
        dt = dateutil.parser.parse("Dec 3 2017 12:00PM")
        time_difference = dt - self.ChannelAge.replace(tzinfo=None)
        time_difference_in_weeks = time_difference.days/7
        self.ChannelAge = time_difference_in_weeks

        '''
        Previous Vid Stats
        '''
        channelSearch = 'https://www.googleapis.com/youtube/v3/search?key=' + self.apikey + '&channelId=' + channelID + "&part=snippet,id&order=date&maxResults=1"
        stats = json.load(urllib2.urlopen(channelSearch))
        lastVidID = stats['items'][0]['id']['videoId'].encode('UTF-8')


        '''
        Stats of last video
        '''

        stats = json.load(urllib2.urlopen(vidStats + lastVidID + '&key=' + self.apikey))
        s = stats['items'][0]['statistics']

        self.prevLikeCount= s['likeCount'].encode('UTF-8')
        self.prevDislikeCount= s['dislikeCount'].encode('UTF-8')
        self.PrevViewCount= s['viewCount'].encode('UTF-8')
        self.prevCommentCount = s['commentCount'].encode('UTF-8')

    def predict(self, WeeksPublished, title_clickbait, nsfw_score):
        '''
        Index([u'subscriberCount', u'channelVideoCount', u'channelViewCount',
       u'PrevCommentCount', u'PrevDislikeCount', u'PrevLikeCount',
       u'PrevViewCount', u'ChannelAge', u'Title-clickbait', u'nsfw_score',
       u'WeeksPublished'],
        '''
        columnNames = ['subscriberCount', 'channelVideoCount', 'channelViewCount', 'PrevCommentCount',
                       'PrevDislikeCount' ,'PrevLikeCount', 'PrevViewCount', 'ChannelAge','Title-clickbait',
                       'nsfw_score', 'WeeksPublished']

        data = np.array([self.subscriberCount, self.channelVideoCount, self.channelViewCount, self.prevCommentCount,
                        self.prevDislikeCount, self.prevLikeCount, self.PrevViewCount, self.ChannelAge, title_clickbait,
                         nsfw_score, WeeksPublished])

        print data
        print len(columnNames)
        print len(data)
        data = data.astype(float)

        X = pd.DataFrame(data = data, index = columnNames).transpose()


        print X.columns.to_series().groupby(X.dtypes).groups
        loaded_model = pickle.load(open("../models/xgb001.pickle.dat", "rb"))
        y_pred = np.exp(loaded_model.predict(X))
        return y_pred[0]

    def printStats(self):
        print "Subscriber Count", self.subscriberCount
        print "Channel Video Count", self.channelVideoCount
        print "Previous Comment Count", self.prevCommentCount
        print "Previous Like Count", self.prevLikeCount
        print "Previous DislikeCout",  self.prevDislikeCount
        print "Previous View Count", self.PrevViewCount
        print "Channel Age in Weeks", self.ChannelAge

fetcher = YoutTubeFetcher(key)
fetcher.get('UChUEb7Fczc6jyXo-R0qnn8Q')
fetcher.predict(2,0.6,0.1)