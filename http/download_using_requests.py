import requests
from time import time

STREAM = False

def download_file(url):

    start = time()
    local_filename = "downloaded"
    r = requests.get(url, stream=STREAM)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)

    duration = time() - start
    print "Took :", duration, "with stream =", STREAM
    return local_filename


download_file("http://localhost:8888/files/")
