import requests
from time import time

STREAM = False

def download_file(url):

    start = time()
    local_filename = "downloaded"
    # NOTE the stream=True parameter
    r = requests.get(url, stream=STREAM)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian

    duration = time() - start
    print "Took :", duration, "with stream =", STREAM
    return local_filename


download_file("http://localhost:8888/files/")
