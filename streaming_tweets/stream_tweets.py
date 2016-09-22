# -*- coding: latin-1 -*-
__author__='Guinsly Mondésir'
__copyrights__=['University of Ottawa']
__version__="1.0.0"
__status__='Production'
__license__='GPL'

#python standard library
import time, uuid, string
import os, io, json, sys
import random
from datetime import datetime
from os import listdir, path, stat
from os.path import isfile, join, exists

#Third party (pip install ...)
import wget
import dropbox
from TwitterAPI import TwitterAPI
import openpyxl

#file in the current directory
from downloads import check_if_user_is_in_the_db, send_email_gmx  # import our task
from downloads import find_by_exactly_this_query, find_this_content  # import our task
from downloads import put_this_into_the_db  # import our task
from logs_to_file import configuration_of_the_logs as set_logs



'''
===============================================
===============================================
My Credentials & Global Variables
===============================================
===============================================
'''
#Dropbox
client = dropbox.client.DropboxClient('0uajGX4uResAAAAAAAAAsKawnzA2TJYc4QweHpfURfjGyO0bfbz_G3EezBc70-n6')

#Twitter
credentials = {'CONSUMER_KEY':'IqFRJBXHUKTeOQQHZpEo8COWD',
				'CONSUMER_SECRET':'S2fNP8vui6KFDp64BcO5ojBMeqLfmZFPtak3a2mIFjP0j1yqvb',
				'ACCESS_KEY':'75557911-OdVGA3g880tC9E7pshwZ5ilwBAWOxrYSDPChmpfje',
				'ACCESS_SECRET':'xR5GWdHbTh7GbGRDSqIYPTiUleKTmzsUfRCsC1rZeXZpS'}

###Loggins
log_this = set_logs()


api = TwitterAPI(
credentials.get('CONSUMER_KEY', None), 
credentials.get('CONSUMER_SECRET', None),
credentials.get('ACCESS_KEY', None),
credentials.get('ACCESS_SECRET', None)
			)

	


'''
===============================================
===============================================
User Lookup
===============================================
===============================================
'''
def read_file():
	"""read file of users
	
	read a file containing all the users
	
	Returns:
		list -- a list of users
	"""
	lines = [line.rstrip('\n') for line in open('users.txt')]
	return lines

def write_this_user_infos_in_a_file(tweets, filename):
	"""Write this users twitter s info into a file
	
	For any given user I will write the infos into a json file
	
	Arguments:
		tweets {dict} -- a dict representing the users infos
		filename {string} -- a filename 
	"""
	with io.open('live_tweets/'+filename+'.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(tweets, ensure_ascii=False, sort_keys = True, indent = 4))
	f = open('live_tweets/'+filename+'.json', 'rb')
	log_this.info('creating a user file = '+ filename +'.json')
	log_this.info('Backup this file into Dropbox = '+ filename+'.json')
	response = client.put_file('/json_files_trial/'+filename+'.json', f)

def do_a_user_lookup(TRACK_TERM):
	  """On twitter retrieves this user info
	  
	  For each user in the list, download his Profile
	  
	  Arguments:
	  	TRACK_TERM {list} -- a list of targeted user took from 
	  	                     read_excel_file()
	  
	  Returns:
	  	{list} -- an empty list of users means that the Profile
	  	          informations of every Users was downloaded 
	  """
	  compte = 0
	  name_of_users = []
	  for users in TRACK_TERM:
	  	  log_this.info('reading info for this users: ' + users)
	  	  try:
	  	  	  r = api.request('users/lookup', {'screen_name': users })
	  	  except:
	  	  	  log_this.warning("Twitter connection error")
	  	  for item in r:
	  	  	  try:
	  	  	  	  compte += 1
	  	  	  	  write_this_user_infos_in_a_file(item, item.get('screen_name'))
	  	  	  	  log_this.info('Retrieved info this user: '+ item.get('screen_name'))
	  	  	  	  check_if_user_is_in_the_db(
	  	  	  	  	item.get('profile_image_url'), item.get('id_str')
	  	  	  	  	)
	  	  	  	  time.sleep(1)
	  	  	  except Exception as e:
	  	  	  	  name_of_users.append(users)
	  	  	  	  log_this.warning('error while retreiving info for this user '+ users)
	  	  	  	  log_this.error(e, exc_info=True)
	  	  	  	  print(name_of_users)
	  	  	  	  return False
	  #if name_of_users is empty it means that I was able to retrieve
	  #all users infos
	  return True


'''
===============================================
===============================================
Main App
===============================================
===============================================
'''


def write_this_tweet_in_a_file(tweets):
	"""Write only one tweet in a file
	
	This function will write the tweet into a JSON file
	This function can be optimize by merging it with 
	write_this_user_infos_in_a_file()
	
	Arguments:
		tweets {dict} -- a dictionnary containing the user tweet
	"""
	filename=str(uuid.uuid4())
	log_this.info('create a file for this tweet :' + filename + '.json')
	with io.open('live_tweets/'+filename+'.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(tweets, ensure_ascii=False, sort_keys = True, indent = 4))
	f = open('live_tweets/'+filename+'.json', 'rb')
	log_this.info('Backup this tweet into Dropbox: '+ filename + '.json')
	response = client.put_file('/json_files_trial/'+filename+'.json', f)

def retrieve_tweets(tweets, TRACK_TERM):
	"""Stream all tweets
	
	[description]
	
	Arguments:
		tweets {list} -- empty (need to remove on prod)
		TRACK_TERM {list} -- a list of all targeted users
	
	Returns:
		bool -- if it's false it means that something went wrong
	"""
	try:
		r = api.request('statuses/filter', {'track': TRACK_TERM})
		for item in r:
			#only one tweets per file
			write_this_tweet_in_a_file(item)
			profile_image_url = item.get('user').get('profile_image_url') 
			id_str = item.get('user').get('id_str') 
			check_if_user_is_in_the_db(profile_image_url , id_str)
			log_this.info('retrieved this user :' + id_str)
			time.sleep(1)
	except Exception as e:
		#check the last time that I added something in the db
		app_log.warning('Error while retrieving tweets')
		app_log.error(e, exc_info=True)
		result = find_by_exactly_this_query("SELECT * FROM `warnings` ORDER BY `id` DESC LIMIT 1")
		if result == None:
			  a = put_this_into_the_db("INSERT INTO `warnings` (`message`, `warnings_type`) VALUES (%s, %s)", ("Erreur de connection à Twitter", 'connection'))
		else:
		    log_this.warning('there is something in the db and something went wrong')
		    #if the last record was inserted today into the dB don't do nothing
		    if ( str(result.get('created_dt')).split(' ')[0] == str(datetime.today().date()) ):
			      #ne fait rien
			      time.sleep(1)
			      return True
		    else:
			      #Otherwise insert a Record into the db AND send me a EMAIL
			      log_this.warning('sms or add a message')
			      time.sleep(15)
			      send_email_gmx('error connection with twitter')
			      time.sleep(1)
			      a = put_this_into_the_db("INSERT INTO `warnings` (`message`, `warnings_type`) VALUES (%s, %s)", ("Erreur de connection à Twitter", 'connection'))
			      return True
		time.sleep(1)
		return True

def start_streaming(TRACK_TERM):
	"""main function to start with
	
	the main function of this application
	
	Arguments:
		TRACK_TERM {list} -- the main function
		         will get the list of targeted Users 
		         will retrieve each users Profile or
		         will start the Streaming

		         While I don't stop the application
		         I want it to retrieve tweets
	"""
	tweets = []
	message = True
	while message:
		message = retrieve_tweets(tweets, TRACK_TERM)
		log_this.warning("Twitter had a glitch I have to restart the connection")

if __name__ == '__main__':
    #TRACK_TERM = read_excel_file()
    #TRACK_TERM.sort(reverse=True)
    #log_this.info('user lookup')
    #do_a_user_lookup(TRACK_TERM)
    #log_this.info('start the real app')
    #main(TRACK_TERM)
    log_this.info('start this application')
    log_this.warning('close -- the end')