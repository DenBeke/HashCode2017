import sys
import collections
import operator

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
        self.videos = list() # videos to be served

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

        for i in range(len(latencies)):
            self.latency_map[caches[i]] = latencies[i]

class Request:
    def __init__(self, request_id, amount, video, endpoint):
        '''
        Initialize request
        '''
        self.id   = request_id
        self.amount = int(amount)      
        self.video = video
        self.endpoint = endpoint
        self.current_latency = endpoint.datacenter_latency
        self.temp_score = 0


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




class Score:
    def __init__(self, cache, video):
        self.id = str(cache.id) + "-" + str(video.id)
        self.cache = cache
        self.video = video
        self.score = 0


scores = dict() #score_id to score
"""
print("START")
for request in requests:
    for cache in request.endpoint.caches:

        score_id = str(cache.id) + "-" + str(request.video.id)
        if score_id in scores:
            prev_score = scores[score_id]
        else:
            prev_score = Score(cache, request.video)
            scores[score_id] = prev_score
        
        prev_score.score += request.amount * (endpoint.datacenter_latency - request.endpoint.latency_map[cache])
print ("SCORED REQUESTS")
remaining = dict()
for cache in caches:
    remaining[cache] = config.capacity

scores_list = scores.values()
print("SORTING SCORES")
sorted_scores = sorted(scores_list, key=operator.attrgetter('score'), reverse=True)
print("SORTED SCORES")

for score in sorted_scores:

    this_remaining = remaining[score.cache]
    this_size = score.video.size
    if this_remaining < this_size:
        continue
    score.cache.videos.append(score.video)
    remaining[score.cache] = this_remaining - this_size


print(generateResult(caches), end="")
"""

W1 = 1000
W2 = 1
W3 = 1

def latency_gain(cache, request):
    return request.current_latency - request.endpoint.latency_map[cache]

while True:
    assigned = False
    #print("MAINLOOP")
    for cache in caches:
        #print("CACHE")
        these_requests = list()
        cur_highest_request = None
        cur_highest_score = 0
        for request in requests:
            if cache not in request.endpoint.caches:
                continue
            if request.video.size > cache.size:
                continue
            if request.video in cache.videos:
                continue

            these_requests.append(request)
            request.temp_score = W1 * (1 / request.video.size) + W2 * request.amount + W3 * latency_gain(cache, request)

            if request.temp_score > cur_highest_score:
                cur_highest_score = request.temp_score
                cur_highest_request = request


        if cur_highest_request is not None:

            assigned = True

            cache.videos.append(cur_highest_request.video)
            cache.size -= cur_highest_request.video.size
            
            for request in these_requests:
                if request.video == cur_highest_request.video:
                    new_latency = request.endpoint.latency_map[cache]
                    if request.current_latency > new_latency:
                        request.current_latency = new_latency


    if not assigned:
        break 

print(generateResult(caches), end="")
    
