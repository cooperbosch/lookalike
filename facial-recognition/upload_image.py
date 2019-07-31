from imgurpython import ImgurClient
client_id='63eed5a21e916ae'
client_secret='b21fa9be5a4dcd6ec618c6a97733c2a5427abf59'
client=ImgurClient(client_id,client_secret)
def upload(filepath):
    image=client.upload_from_path(filepath,config=None,anon=True)
    return image["link"]
