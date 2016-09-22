# -*- coding: latin-1 -*-
__author__='Guinsly Mondésir'
__copyrights__=['University of Ottawa']
__version__="1.0.0"
__status__='Production'
__license__='GPL'

#python standard library
import shutil
import sys
import os
from os import listdir, path
from os.path import isfile, join, exists
from datetime import datetime
import smtplib

#third-party (pip install ...)
import pymysql.cursors
import dropbox
from PIL import Image
import imagehash
import wget


#file in the current directory
from logs_to_file import configuration_of_the_logs as set_logs

log_this = set_logs()


client = dropbox.client.DropboxClient('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

def send_email_gmx(msg):
	server = smtplib.SMTP('smtp.gmx.com:587')
	server.starttls()
	server.login('email@example.com','hjljhlhjlhl')
	server.sendmail('email@example.com', 'other_email@example.com', msg)
	server.quit()

'''
=============================================================================
=============================================================================
=============================================================================
=============================================================================
=============================================================================
=============================================================================
=============================================================================
=============================================================================
=============================================================================
=============================================================================
'''

def find_by_exactly_this_query(query):
    """find the result of this query

    For a given query find the result
    Note: The next 2 function can be optimize in one function

    Arguments:
      query {string} -- the sql query

    Returns:
      bool or list -- list or Result or
                      False
    """
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='(drElizabeth)',
                             db='communications',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = query
            cursor.execute(sql)
            result = cursor.fetchone()
    except Exception as e:
        connection.close()
        return False
    #else
    connection.close()
    return result



def find_this_content(query, param):
    """find this query with this params

    note : find_by_exactly_this_query

    Arguments:
      query {string} -- the query
      param {list} -- the arguments of the MYSQL query

    Returns:
      [type] -- [description]
    """
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='(drElizabeth)',
                             db='communications',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = query
            cursor.execute(sql, (param,))
            result = cursor.fetchone()
    except Exception as e:
        print(e)
        connection.close()
        return False
    #else
    connection.close()
    return result


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
                                 password='(drElizabeth)',
                                 db='communications',
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


def download_images(image_url):
	hash = ''
	original_hash = ''
	try:
		#download the normal size
		extension = image_url.split('.')[-1]
		filename = wget.download(image_url)
		log_this.info("downloading this image " + image_url)
		f = open(filename, 'rb')
		response = client.put_file('/pictures_trial/'+filename, f)
		hash = create_hash(image_url.split('/')[-1])
		#download original size
		image_url = image_url.split('_normal')[0]
		filename = image_url + '.' + extension
		filename = wget.download(filename)
		f = open(filename, 'rb')
		response = client.put_file('/pictures_trial/'+filename, f)
		original_hash = create_hash(filename)
	except:
		print('error on this url')
		print(image_url)
	finally:
		return {'normal_hash': hash, 'original_hash': original_hash}

def create_hash(image_name):
	  hash = imagehash.average_hash(Image.open(image_name))
	  return str(hash)

def move_the_images():
    """move the images into the pictures folder

    move the images into the pictures folders
    """
    #Loop through file in the current directory
    images_extensions = ['jpeg', 'jpg', 'png', 'gif', 'GIF',
                          'JPG', 'JPEG', 'PNG', 'bmp', 'BMP']
    my_path = path.dirname(path.realpath(__file__))
    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    for fichier in onlyfiles:
        if (fichier.split('.')[-1] in images_extensions) or ('_normal' in fichier):
            shutil.move(join(my_path, fichier), join(my_path+"/pictures/", fichier))

def download_images_and_put_datas_in_the_db(user_id, image_url):
    """download_images_and_put_datas_in_the_db

    Will download the images and put the Hash value into the db

    Arguments:
      user_id {[type]} -- [description]
      image_url {[type]} -- [description]
    """
    result = download_images(image_url)
    query = "INSERT INTO `users` (`twitter_user_id`, `profile_image_url`, `normal_image_profile_hash`, `original_image_profile_hash`) VALUES (%s, %s, %s, %s)"
    params = (user_id, image_url, result['normal_hash'], result['original_hash'])
    put_this_into_the_db(query, params)
    move_the_images()

def check_if_user_is_in_the_db(image_url, user_id):
    """Check if the user'profile hash value is in the db

    If the user is already in the db check if it's has the same image

    Arguments:
      image_url {[type]} -- [description]
      user_id {[type]} -- [description]
    """
    #connect to see if the USER_ID is in the DATABASE
    response = find_this_content("SELECT `id`, `twitter_user_id`, `normal_image_profile_hash`, `profile_image_url` FROM `users` WHERE `twitter_user_id`=%s ORDER BY `id` DESC LIMIT 1", user_id)
    if response == None:
        download_images_and_put_datas_in_the_db(user_id, image_url)
        log_this.info('putting this user_id in the db '+ user_id)
        #move the images
    #if we have found the USER
    else:
        #print('I found it')
        #I'm guessing that Twitter will change the image filename ( Need to check this)
        same_image = image_url.split('/')[-1] == (response['profile_image_url']).split('/')[-1]
        #if False (download image and insert a new record in the database)
        if same_image == False:
            log_this.info('not the same images')
            download_images_and_put_datas_in_the_db(user_id,image_url)
        log_this.info('same image nothing to do :(')

if __name__ == '__main__':
      #check_if_user_is_in_the_db("http://pbs.twimg.com/profile_images/577841064767201280/rc2wvWxK_normal.jpeg", "107485339")
      #check_if_user_is_in_the_db("http://pbs.twimg.com/profile_images/694662257586892802/mdc5ELjj_normal.jpg", "107485339")
      #put_this_into_the_db("INSERT INTO `warnings` (`message`, `warnings_type`) VALUES (%s, %s)", ("Hello  there is a critical error", 'connection'))
      a = find_by_exactly_this_query("SELECT * FROM `warnings` ORDER BY `id` DESC LIMIT 1")
      print(str(a.get('created_dt')).split(' ')[0] == str(datetime.today().date()))
      print(datetime.today())
      print(type(a.get('created_dt')))


'''
create database communications;
use communications;


CREATE TABLE `users` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`twitter_user_id` varchar(40) COLLATE utf8_bin NOT NULL,
`twitter_handle` varchar(60) COLLATE utf8_bin NOT NULL,
`profile_image_url` varchar(255) COLLATE utf8_bin NOT NULL,
`normal_image_profile_hash` varchar(255) COLLATE utf8_bin NOT NULL,
`original_image_profile_hash` varchar(255) COLLATE utf8_bin NOT NULL,
`updated_dt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;


CREATE TABLE `warnings` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`message` MEDIUMTEXT COLLATE utf8_bin NOT NULL,
`warnings_type` varchar(25) COLLATE utf8_bin NOT NULL,
`created_dt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
'''
