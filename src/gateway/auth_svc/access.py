#access.py for gateway service


import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials",401)
    
    basicAuth=(auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESSS')}/login", #reads from auth's server.py; requests server to read
        auth=basicAuth #credentials for server to verify 
    )
    
    if response.status_code==200:
        return response.text, None
    else:
        return None, (response.text,response.status_code) 


