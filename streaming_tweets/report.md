#Report

This document represent my analysis of the the two options that you send me by email [twitter-python](https://github.com/computermacgyver/twitter-python) and [ELXN42-Article] (https://github.com/web-archive-group/ELXN42-Article/blob/master/elxn42.md)

##Twitter api
Twitter can close the connection to its API for numerous reason i.e. The Twitter team wants to update something on their API. This list represent the different [status code](https://dev.twitter.com/overview/api/response-codes) Any **status code** between the range 400 to 504 can cause Twitter to shutdown the Streaming connection (or a Search request). We did experience some glich in the connection not in our application code itself but by Twitter. Now we will see how does the github repos that you gave me deal with those Twitter exception or errors.

###[ELXN42-Article] (https://github.com/web-archive-group/ELXN42-Article/blob/master/elxn42.md)
They conduct two types of Research one by **searching** some string values on Twitter and the other by **streaming** a list of values. This team uses the [twarc](https://github.com/edsu/twarc)command line. Here is what they have to deal with

> However, we noticed that twarc had silently failed during September, and the research team did not notice. We believe the failure here was because of an issue with the Twitter API or network connection issues, but it is not clear, and we are not confident as to why we had a silent failure. **As a result we lost 27 days in total**. Upon realization of the collection failure, the research team immediately began collecting via the stream API...

this was taken in their github page within the second paragraph titled **Creating your Own Twitter Archive: Data Collection** I believe they were talking about their streaming application. Our approach that we took in your research is to restart the application within 30 seconds and this is way less time then waiting **27 days** to restart the streaming. We also logs each time that the application had an error. 

###[twitter-python](https://github.com/computermacgyver/twitter-python)
Twitter-python is a collection of python scripts' helper build on top of [tweepy](https://github.com/tweepy/tweepy) to achieve what we are doing in your Research. Meaning that it can search or stream on Twitter. Upon examination I realize that they use a similar approach as I did. Meaning that upon an error the application will restart by itself and it may send an email. I will explain their approach in the following lines.

**[streaming.py]**(https://github.com/computermacgyver/twitter-python/blob/master/streaming.py) is the name of the script that does what we are aiming to do in your Research. Each day they will produce a file containing all the JSON object of the present day. Meaning that for some given usernames, this application will produce one JSON file containing all the direct tweet. So this JSON file can have 0 to 5000 tweets and the next day it will produce another one. Overall this script **streaming.py** is pretty solid (or good).

There is **3 types of errors** that this script (streaming.py) can deal with. **KeyboardInterrupt** that when the user (like me) wants to stop the execution of the script. **TimeoutException** that represent upon the first connection to Twitter if there is an error like the application wait 60 sec instead of 1 sec to connect to Twitter, this exception will stop and try to connect again to Twitter. My understanding is that this error must be on the server side meaming that it's not twitter's fault but our own machine, our own internet connection is not working because **tweepy** didn't implement this Exception. The last exception deal with every other kind of error that might occurs (like our TwitterConnection) this application will send a email to the owner and will try to reconnect to twitter after **1800 seconds** meaning after 30 minutes. So this is still way far from our 30 secs wait time. Here is a snippet of their code.

```python
	while True:
		try:
			#Connect to the Twitter stream
			stream = Stream(auth, listener)
			#Strart streaming with the usersname (screen_name)
			stream.filter(track=terms)

		except KeyboardInterrupt:
			#User pressed ctrl+c or cmd+c -- get ready to exit the program
			print("%s - KeyboardInterrupt caught. Closing stream and exiting."%datetime.now())
			listener.close()
			stream.disconnect()
			break
		except TimeoutException:
			#Timeout error, network problems? reconnect.
			print("%s - Timeout exception caught. Closing stream and reopening."%datetime.now())
			try:
				listener.close()
				stream.disconnect()
			except:
				pass
			continue
		except Exception as e:
			#Anything else
			try:
				info = str(e)
				sys.stderr.write("%s - Unexpected exception. %s\n"%(datetime.now(),info))
				msg = MIMEText("Unexpected error in Twitter collector. Check server. %s"%info);
				msg['Subject'] = "Unexpected error in Twitter collector"
				msg['From'] = "youremail@example.com"
				msg['To'] = email
				s = smtplib.SMTP("smtp.example.com") #Update this to your SMTP server
				s.sendmail("youremail@example.com", email, msg.as_string())
				s.quit()
			except:
				pass
			time.sleep(1800)#Sleep thirty minutes and resume
```

#Conclusion
So in my understanding both github repos that you gave me had to deal with errors (Exceptions). And I do believe that waiting 30 seconds is way less then waiting **30 min** or waiting **27 days** before restarting the application. Also the streaming connection to Twitter has some glitch not on our side but on their side. But I'm not even quite so sure that it's on Twitter' side because I remember that, before our first appointment back in late March when I first tried to stream 200 random usernames for two days I didn't have any connections errors back then.

#Future task
	1. Should I start streaming tomorrow (Wednesday 18th or June 18th) as we conclude on our last meeting?
	2. Do you want I to use the **streaming.py** script from the **twitter-python** instead of ours and modifyied the 30 minutes to 1 min. or 30 sec.
		1. In the light of my understanding of research I noticed that you wanted to use the same approach (same script) as an other research team did





