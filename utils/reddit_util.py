import praw

def initialize_reddit(config):
    client_id = config['REDDIT']['CLIENT_ID']
    client_secret = config['REDDIT']['CLIENT_SECRET']
    password = config['REDDIT']['PASSWORD']
    username = config['REDDIT']['USERNAME']

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        username=username,
        user_agent='Reddit Award Compiler v1.0 by ARandomBoiIsMe'
    )
