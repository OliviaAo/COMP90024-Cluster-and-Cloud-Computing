
import tweepy 
import json
from time import sleep
from TwitterAPI import TwitterAPI
from tweepy.streaming import StreamListener

# Variables that contains the user credentials to access Twitter API
consumer_key = 'aMlAt9xTsFOxaD11InOfeo8NV'
consumer_secret = '37pfRhPJKSyZcCNPPJUfaoJxVhWobaqkSkR8oQobnkCQ5g3Et8'
access_token_key = '851934201506971648-H5d9b02jl5AdCG0eOm2EoZbXNq0xY4K'
access_token_secret = 'yKlL4K5PB4g9YDqWDzDAcu2AOzSDQNs3gZAYpdOUs3b6A'

# Create a class inheriting from StreamListener
class TwitterStream(StreamListener):
    
    def __init__( self, api = None, ):
        self.api = api

    def on_data( self, data ):
        print "hello~~~~~~~~!!!"
        if 'in_reply_to_status' in data:
            self.on_status( data )
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete( delete['id'], delete['user_id'] ) is False:
                return False
        elif 'limit' in data:
            if self.on_limit( json.loads(data)['limit']['track'] ) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status( self, status ):
        print status
        # print remaining 

    def on_error( self, status ):
        if status == 420:
            print status
            self.on_timeout()

    ''' Rate Limit '''
    def on_timeout( self ):
        print("~~~~~~~~Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 


   
       



   



        
        
        
        
        
        
        
        
        
        
        
        
        
