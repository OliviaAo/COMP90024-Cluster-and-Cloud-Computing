    

from TwitterStream import TwitterStream
import time, tweepy, sys
from time import sleep

## authentication
# consumer_key = 'aMlAt9xTsFOxaD11InOfeo8NV'
# consumer_secret = '37pfRhPJKSyZcCNPPJUfaoJxVhWobaqkSkR8oQobnkCQ5g3Et8'
# access_token_key = '851934201506971648-H5d9b02jl5AdCG0eOm2EoZbXNq0xY4K'
# access_token_secret = 'yKlL4K5PB4g9YDqWDzDAcu2AOzSDQNs3gZAYpdOUs3b6A'

consumer_key = 'nyR8ejR7Z7LftoDYRoyusn2jg'
consumer_secret = 'lLlxxKAOd3DyIGTLVgq1Mwy8hOnsGPCTroBhAIbgqB31Dbp0WT'
access_token_key = '851934201506971648-TTEeRvC5pcTBu5GGl9LV1yqANvRMVu1'
access_token_secret = 'tyZVYaNiPm2bMjjo4bkEuGwABUHoBITlrnWnDEENqKZSl'
    
auth = tweepy.OAuthHandler( consumer_key, consumer_secret )
auth.set_access_token( access_token_key, access_token_secret )
api = tweepy.API( auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True )
def stream_crawl( keyword ):
        
    loop = True
    while ( loop ):
        track = keyword
        listen = TwitterStream( api )  
        stream = tweepy.Stream( auth,listen )

        # Starting a Stream
        # stream.filter(track=['python'])

        print ("Twitter streaming started... ")
        try:
            # stream.filer( track = track )
            stream.filter(track=['python'])
            loop = False
        except:
            print ("Error!...And Retry after 60 sec")
            loop = True
            stream.disconnect()
            sleep( 5 )
            continue

if __name__ == '__main__': 
    stream_crawl( "python" )





