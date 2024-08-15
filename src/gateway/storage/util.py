import pika, json

def upload(f, fs, channel,access):
    try:
        fid = fs.put(f) #fid is file-id; fid here is an fid object, not just string
    except Exception as err:
        return "internal server error", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try: 
        channel.basic_publish(
            exchange="", #default exchange
            routing_key="video", #name of queue bc of default exchange?
            body=json.dumps(message), #converts python object into json string
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE #ensures that message in queue persist when pod crash or pod restart
            )
        ) 

    except:
        fs.delete(fid)
        return "internal server error", 500

    """
        1. Upload file to mongodb database
        2. Put a message in rabbitmq queue that tells downstream service to process the upload by pulling from mongodb

    """