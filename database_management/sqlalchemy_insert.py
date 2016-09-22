# -*- coding: latin-1 -*-
__author__='Guinsly Mondésir'
__copyrights__=['University of Ottawa']
__version__="1.0.0"
__status__='Production'
__license__='GPL'

import json
import os
from os import listdir
from os.path import isfile, join
from os import sep, getcwd
import fnmatch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mean_tweets_variables import (
    Tweet, Base, User, Mention, Coordinate, Picture,
    Hashtag, Url, create_table,
    create_table,
    Image
    )
from dateutil.parser import parse
from datetime import datetime

import pymysql
engine = create_engine('mysql+pymysql://root:root@localhost/elizabeth?charset=utf8')
Base.metadata.bind = engine

#import pymysql
#pip install PyMySQL

#pip install timeago
import timeago

DBSession = sessionmaker(bind=engine)
session = DBSession()

mypath = os.path.dirname(os.path.realpath(__file__))


def read_file():
    """read file of users

    read a file containing all the users

    Returns:
    	list -- a list of users
    """
    lines = [line.rstrip('\n') for line in open('users.txt')]
    lines = [line.lower() for line in lines]
    return lines

LIST_OF_USERS = read_file()


def check_if_it_s_null(value):
    """
    Check if it's an Object or not
    a = {"hashtags": []}
    a == NoneType
    """
    if type(value).__name__ == 'NoneType':
        return 0
    else:
        return 1

def get_all_the_json_files():
    """
    """
    #use fnmatch instead
    myfolder = 'live_tweets'
    onlyfiles = [f for f in listdir(mypath + os.sep + myfolder) if isfile(join(mypath +  os.sep + myfolder, f))]
    #onlyjson = [f for f in onlyfiles if f.split('.')[1] == 'json']
    onlyjson = [f for f in onlyfiles if fnmatch.fnmatch(f, '*.json') and len(f) > 25]
    return onlyjson


def get_the_json_value(filename):
    """
    open the file and get the content
    """
    filename = 'live_tweets/' + filename
    print(filename)
    with open(filename, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return(data)

'''
    created_at = Column(DateTime)
'''
def create_new_user(data):
    """
    insert new user into db
    """
    #user
    user_id = data.get('user').get('id_str')
    new_user = session.query(User).filter(User.id_str == user_id).first()
    if new_user is None:
        s_name = (data.get('user').get('screen_name'))
        user_name = (data.get('user').get('name'))
        time_zone = data.get('user').get('time_zone')
        location = data.get('user').get('location')
        default_profile = data.get('user').get('default_profile')
        default_profile_image = data.get('user').get('default_profile_image')
        favourites_count = data.get('user').get('favourites_count')
        listed_count = data.get('user').get('listed_count')
        followers_count = data.get('user').get('followers_count')
        statuses_count = data.get('user').get('statuses_count')
        friends_count = data.get('user').get('friends_count')
        location = data.get('user').get('location')
        screen_name = data.get('user').get('screen_name')
        description = (data.get('user').get('description'))
        profile_url = "https://www.twitter.com/" + s_name
        created_at = parse(data.get('created_at'))
        if s_name.lower() in LIST_OF_USERS:
            targeted = 1
        else:
            targeted = 0
        new_user = User(
            id_str=user_id, targeted=targeted,
            name=user_name.lower(),location=location,
            screen_name=s_name.lower(), time_zone=time_zone,
            default_profile=default_profile,
            default_profile_image=default_profile_image,
            favourites_count=favourites_count,
            listed_count=listed_count,followers_count=followers_count,
            statuses_count=statuses_count,
            friends_count=friends_count, description=description,
            profile_url=profile_url, created_at=created_at
            )
        session.add(new_user)
        session.commit()
        #creating a profile
    return new_user



"""
    created_at = Column(DateTime)
"""
def create_new_tweet(data, new_user, filename):
    """
    insert new tweet into db
    """
    #tweet
    tweet_id = data.get('id_str')
    language = data.get('lang')
    tweet_text = (data.get('text')).encode('unicode-escape')
    in_reply_to_user = data.get('in_reply_to_user_id_str')
    geo_location = check_if_it_s_null(data.get('geo'))
    coordinates = check_if_it_s_null(data.get('coordinates'))
    created_at = parse(data.get('created_at'))
    new_tweet = Tweet(tweet_id_str=tweet_id, tweet=tweet_text,
                lang=language,created_at=created_at,
                geo=geo_location,filename=filename,
                coordinates=coordinates,
                in_reply_to_user_id_str=in_reply_to_user,
                user=new_user)
    session.add(new_tweet)
    session.commit()
    #Create coordinate table
    #if coordinates:
    #create_new_coordinates(data, new_tweet)
    return new_tweet


def put_this_into_the_db(query, param):
    """put this value into the database

    see : find_by_exactly_this_query()

    Arguments:
      query {[type]} -- [description]
      param {[type]} -- [description]

    Returns:
      bool -- [description]
    """
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='elizabeth',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = query
            cursor.execute(sql, param)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        print(e)
        connection.close()
        return False
    connection.close()
    return True

def insert_data_into_the_picture_table():
    beginning = datetime.now()
    compte = 0
    with open('user_pictures.json', encoding='utf-8') as data_file:
        data = json.load(data_file)

    for information in data[:]:
        now = datetime.now()
        twitter_user_id = information.get('twitter_user_id')
        user = session.query(User).filter(User.id_str == twitter_user_id).first()
        if user:
            print("found - {0}".format(twitter_user_id))
            original_image_profile_hash = information.get('original_image_profile_hash')
            normal_image_profile_hash = information.get('normal_image_profile_hash')
            profile_image_url = information.get('profile_image_url ')
            created_at = parse(information.get('created_at'))
            #manual way
            query = "INSERT INTO `image` (`original_image_profile_hash`, `normal_image_profile_hash`, `profile_image_url`, `created_at`, `user_id_str` ) VALUES (%s, %s, %s, %s, %s)"
            params = (original_image_profile_hash,normal_image_profile_hash,profile_image_url,created_at, str(twitter_user_id))
            put_this_into_the_db(query, params)
            """
            new_picture = Picture(
            user = user,
            original_image_profile_hash = original_image_profile_hash,
            normal_image_profile_hash = normal_image_profile_hash,
            profile_image_url = profile_image_url,
            created_at = created_at
            )
            session.add(new_picture)
            session.commit()
            session.flush()
            """
            compte += 1
        else:
            #print("{0} Not found: {1}".format('-'*3, twitter_user_id))
            pass
    print("{0}/{1}: number of inserted document".format(compte, len(data)))
    '''
    80121/39582: number of inserted document
    55 minutes ago
    '''
    '''
    print(session.query(Picture).count())
    print(session.query(Picture).first().id)
    print(engine)
    '''
    print (timeago.format(beginning, now))

def create_new_mention(data, new_tweet):
    """
    insert new mention into db
    """
    #Mention
    mentions = data.get('entities').get('user_mentions')
    if mentions:
        for value in mentions:
            #mention_id = (value.get('id'))
            mention_name = (value.get('name'))
            mention_s_name = (value.get('screen_name')).lower()
            new_mention = Mention(
            name=mention_name,
            tweet_id_str=new_tweet.tweet_id_str,
            screen_name=mention_s_name,
            tweet=new_tweet
            )
            session.add(new_mention)
            session.commit()


def create_new_coordinates(data, new_tweet):
    """
    insert new hashtags into db
    """
    #Mention
    coordinates = data.get('coordinates')
    if coordinates:
        for value in coordinates:
            longitude, latitude = value.get('coordinates')
            new_coordinate = Coordinate(longitude=longitude,
                        latitude=latitude,
                        tweet_id_str=new_tweet.tweet_id_str,
                         tweet=new_tweet
             )
            session.add(new_coordinate)
            session.commit()

def create_new_hashtags(data, new_tweet):
    """
    insert new hashtags into db
    """
    #Mention
    hashtags = data.get('entities').get('hashtags')
    if hashtags:
        for value in hashtags:
            h_text = (value.get('text'))
            new_hashtag = Hashtag(text=h_text, tweet=new_tweet,
            tweet_id_str=new_tweet.tweet_id_str,)
            session.add(new_hashtag)
            session.commit()

def create_new_urls(data, new_tweet):
    """
    insert new urls into db
    """
    #Mention
    urls = data.get('entities').get('urls')
    if urls:
        for value in urls:
            e_url = (value.get('expanded_url'))
            s_url = (value.get('url'))
            new_url = Url(shortened_url=s_url,
            expanded_url=e_url,
            tweet_id_str=new_tweet.tweet_id_str,
            tweet=new_tweet)
            session.add(new_url)
            session.commit()

def parse_value(data, filename):
    """
    """
    #user
    new_user = create_new_user(data)
    #tweet
    new_tweet = create_new_tweet(data, new_user, filename)
    create_new_mention(data, new_tweet)
    create_new_hashtags(data, new_tweet)
    create_new_urls(data, new_tweet)

def parse_each_file(onlyjson):
    """
    Insert the content of the file into the DB
    """
    total_file = len(onlyjson)
    beginning = datetime.now()
    for i in onlyjson:
        now = datetime.now()
        print(str(onlyjson.index(i)) + ' / ' + str(total_file))
        data = get_the_json_value(i)
        parse_value(data, i)
        print (timeago.format(beginning, now))

if __name__ == '__main__':
    #todo:
    ##need to add comments
    create_table()
    json_files = get_all_the_json_files()
    parse_each_file(json_files)
    insert_data_into_the_picture_table()
