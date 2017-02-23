import sys

class Config:
    def __init__(self, line):
        '''
        Initialize config struct based on input line
        '''
        self.videos               = int(line[0])
        self.endpoints            = int(line[1])
        self.request_descriptions = int(line[2])
        self.cache_servers        = int(line[3])
        self.capacity             = int(line[4])


class Video:
    def __init__(self, video_id, size):
        '''
        Initialize video
        '''
        self.id   = video_id
        self.size = int(size)

class Cache:
    def __init__(self, cache_id, size):
        '''
        Initialize caching server
        '''
        self.id   = cache_id
        self.size = int(size)

class Endpoint:
    def __init__(self, endpoint_id, datacenter_latency, caches, latencies):
        '''
        Initialize endpoint
        '''
        self.id   = endpoint_id
        self.datacenter_latency = int(datacenter_latency)
        self.caches = caches
        self.latencies = latencies # respective latencies to caches

class Request:
    def __init__(self, request_id, amount, video_id, endpoint_id):
        '''
        Initialize request
        '''
        self.id   = request_id
        self.amount = int(amount)      
        self.video_id = int(video_id)
        self.endpoint_id = int(endpoint_id)

videos = list()
caches = list()
endpoints = list()
requests = list()


# Read line from std in
line = sys.stdin.readline().split()

config = Config(line)


for cache in range(0, config.cache_servers):
    caches.append(Cache(cache, config.capacity))

line = sys.stdin.readline().split()
for video in range(0,config.videos):
    videos.append(Video(video ,line[video]))


for endpoint in range(0, config.endpoints):
    line = sys.stdin.readline().split()
    datacenter_latency = int(line[0])
    num_caches = int(line[1])
    endpoint_caches = list()
    endpoint_latencies = list()
    for cache in range(0, num_caches):
        line = sys.stdin.readline().split()
        endpoint_caches.append(caches[int(line[0])])
        endpoint_latencies.append(int(line[1]))
    endpoints.append(Endpoint(endpoint, datacenter_latency, endpoint_caches, endpoint_latencies))
    

for request in range(0, config.request_descriptions):
    line = sys.stdin.readline().split()
    requests.append(Request(request, line[2], line[0], line[1]))


print(requests[0].id)
print(requests[0].amount)
print(requests[0].video_id)
print(requests[0].endpoint_id)