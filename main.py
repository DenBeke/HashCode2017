import sys
import heapq

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


    def __lt__(self, other):
        return self.id < other.id

class Cache:
    def __init__(self, cache_id, size):
        '''
        Initialize caching server
        '''
        self.id   = cache_id
        self.size = int(size)
        self.videos = list() # videos to be served
        self.usage = 0


    def getFreeSpace(self):
        return self.size - self.usage

    def addVideo(self, video):
        if video in self.videos:
            return True

        if self.usage + video.size > self.size:
            return False

        self.videos.append(video)
        self.usage += video.size

        return True

class Endpoint:
    def __init__(self, endpoint_id, datacenter_latency, caches, latencies):
        '''
        Initialize endpoint
        '''
        self.id                 = endpoint_id
        self.datacenter_latency = int(datacenter_latency)
        self.caches = caches
        self.latencies = latencies # respective latencies to caches
        self.latency_map = dict()
        self.requests = list()
        self.total_requests = 0

        self.popularity = 0

        self.videoQueue = []

        for i in range(len(latencies)):
            self.latency_map[caches[i]] = latencies[i]

        self.sorted_latency_list = [(k, self.latency_map[k]) for k in sorted(self.latency_map, key=self.latency_map.get, reverse=False)]

    def getClosestCache(self, size):
        for (cache, latency) in self.sorted_latency_list:
            if cache.getFreeSpace() >= size:
                return cache

        return None

    def __lt__(self, other):
        return self.id < other.id

class Request:
    def __init__(self, request_id, amount, video, endpoint):
        '''
        Initialize request
        '''
        self.id   = request_id
        self.amount = int(amount)
        self.video = video
        self.endpoint = endpoint


def generateResult(caches):
    out = ""
    count = 0
    for cache in caches:
        if len(cache.videos) == 0:
            continue
        out += str(cache.id) + " "
        for video in cache.videos:
            out += str(video.id) + " "
        out += "\n"
        count += 1

    out = str(count) + "\n" + out
    return out.strip('\n')





videos    = list()
caches    = list()
endpoints = list()
requests  = list()


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
    requests.append(Request(request, line[2], videos[int(line[0])], endpoints[int(line[1])]))


for request in requests:
    endpoint = request.endpoint
    video = request.video

    endpoint.requests.append(request)
    endpoint.total_requests += request.amount




#print(requests[0].id)
#print(requests[0].amount)
#print(requests[0].video)
#print(requests[0].endpoint)


#print(endpoints[0].total_requests)


#print(generateResult(caches), end="")


# count total global requests
total_requests = 0
for endpoint in endpoints:
    total_requests += endpoint.total_requests

# calculate popularity per regio
for endpoint in endpoints:
    endpoint.popularity = endpoint.total_requests / total_requests



# insert endpoints in priority queue
endpointQueue = []
for endpoint in endpoints:
    for request in endpoint.requests:
        # maybe use global total requests instead of endpoint.total_requests
        heapq.heappush(endpoint.videoQueue, (1 - request.amount / endpoint.total_requests, request.video))
    heapq.heappush(endpointQueue, (1 - endpoint.popularity, endpoint))

while len(endpointQueue) != 0:
    (endpointPopularity, endpoint) = heapq.heappop(endpointQueue)
    #print("ENDPOINT", 1-endpointPopularity, endpoint.id)
    while len(endpoint.videoQueue) != 0:
        (videoPopularity, video) = heapq.heappop(endpoint.videoQueue)
        #print("VIDEO", 1-videoPopularity, video.id)

        closestCache = endpoint.getClosestCache(video.size)
        if closestCache == None:
            continue

        closestCache.addVideo(video)

print(generateResult(caches), end="")
