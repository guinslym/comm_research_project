# -*- coding: latin-1 -*-
__author__='Guinsly Mondésir'
__copyrights__=['University of Ottawa']
__version__="1.0.0"
__status__='Production'
__license__='GPL'


#file in the current directory
from stream_tweets import read_file
from stream_tweets import do_a_user_lookup
from stream_tweets import start_streaming
#file in the current directory
from logs_to_file import configuration_of_the_logs as set_logs
add_this_into_logs = set_logs()


if __name__ == '__main__':
    TRACK_TERM = read_file()
    TRACK_TERM.sort(reverse=True)
    print(len(TRACK_TERM)) # change to log
    add_this_into_logs.info('user lookup')
    value = do_a_user_lookup(TRACK_TERM)
    #print(value)
    add_this_into_logs.info('start this application')
    start_streaming(TRACK_TERM)
    add_this_into_logs.warning('close -- the end')
