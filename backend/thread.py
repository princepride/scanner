import requests
from threading import Thread

url_t = "http://localhost:8000/records/%i"
projectid="320940575449"
location="asia-southeast1"
endpoints = {
	'resnet': '7790119047630159872',
	'ensemble1' : '1',
	'ensemble2' : '2',
	'ensemble3' : '3',
	'ensemble4' : '4',
	'ensemble5' : '5',
	'ensemble6' : '6',
	'ensemble7' : '7',
	'ensemble8' : '8',
	'ensemble9' : '9',
	'ensemble10' : '10',
}
def process_id(id):
    """process a single ID"""
    # fetch the data
    r = requests.get(url_t % id)
    # parse the JSON reply
    data = r.json()
    # and update some data with PUT
    requests.put(url_t % id, data=data)
    return data

def process_range(id_range, store=None):
    """process a number of ids, storing the results in a dict"""
    if store is None:
        store = {}
    for id in id_range:
        store[id] = process_id(id)
    return store
	


def threaded_process_range(nthreads, id_range):
    """process the id range in a specified number of threads"""
    store = {}
    threads = []
    # create the threads
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t = Thread(target=process_range, args=(ids,store))
        threads.append(t)

    # start the threads
    [ t.start() for t in threads ]
    # wait for the threads to finish
    [ t.join() for t in threads ]
    return store