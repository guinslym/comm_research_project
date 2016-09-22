# -*- coding: utf-8 -*-
import os
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class TimestampMixin(object):
    created = Column(DateTime, default=datetime.now())

class User(Base, TimestampMixin):
    '''
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    screen_name = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    profile_url = Column(String(250))
    time_zone = Column(String(60))
    created_at = Column(DateTime)
    location = Column(String(60))
    id_str =  Column(String(30))
    default_profile = Column(Integer)
    #is it a targeted user
    targeted = Column(Integer)
    default_profile_image = Column(Integer)
    type_of_image = Column(String(60))
    favourites_count = Column(Integer)
    listed_count = Column(Integer)
    followers_count = Column(Integer)
    statuses_count = Column(Integer)
    friends_count = Column(Integer)
    verified = Column(Integer)

class Tweet(TimestampMixin, Base):
    '''
    t_geo = Deprecated. use Coordinate
    '''
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    tweet_id_str = Column(String(60))
    tweet = Column(String(250), nullable=False)
    lang = Column(String(7))
    in_reply_to_user_id_str = Column(String(60))
    geo = Column(Integer)
    coordinates = Column(Integer)
    user_id_str =  Column(String(30))
    filename = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Picture(TimestampMixin, Base):
    '''
    This table is used to store the hash value of a Picture.
    If a user have changed his Picture than the Hash value
    will be different.

    To check if a user have changed is picture.
    Create a JOIN query where a User has more than one Picture.
    '''
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    original_image_profile_hash = Column(String(60))
    normal_image_profile_hash = Column(String(60))
    profile_image_url = Column(Text)
    user_id_str =  Column(String(30))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Image(TimestampMixin, Base):
    '''
    This table is used to store the hash value of a Picture.
    If a user have changed his Picture than the Hash value
    will be different.

    To check if a user have changed is picture.
    Create a JOIN query where a User has more than one Picture.
    '''
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    original_image_profile_hash = Column(String(60))
    normal_image_profile_hash = Column(String(60))
    profile_image_url = Column(Text)
    user_id_str =  Column(String(30))
    user_id =  Column(Integer)

class Mention(TimestampMixin, Base):
    __tablename__ = 'mention'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    screen_name = Column(String(250), nullable=False)
    tweet_id_str = Column(String(60))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Hashtag(TimestampMixin, Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    tweet_id_str = Column(String(60))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Url(TimestampMixin, Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    expanded_url = Column(Text, nullable=False)
    shortened_url = Column(String(250), nullable=False)
    tweet_id_str = Column(String(60))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)


class Coordinate(TimestampMixin, Base):
    __tablename__ = 'coordinates'
    id = Column(Integer, primary_key=True)
    longitude = Column(String(250))
    latitute = Column(String(250))
    #type coordinate = 'Point'
    t_coordinates = Column(String(60))
    tweet_id_str = Column(String(60))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

def create_table(dbname="dr_elizabeth_research.db"):
    try:
        os.remove(dbname)
    except:
        pass
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///'+dbname)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_table()
