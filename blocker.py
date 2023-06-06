from mitmproxy import http
from mitmproxy import ctx

class Blocker:
    def __init__(self):
        # Read filters from file
        with open('filtered_sites.txt', 'r') as file:
            self.filters = [line.strip() for line in file]

    def request(self, flow: http.HTTPFlow) -> None:
        host = flow.request.host
        for filter in self.filters:
            if '*' in filter:
                # Handle wildcard filters
                filter_parts = filter.split('.')
                host_parts = host.split('.')
                if len(host_parts) == len(filter_parts):
                    match = True
                    for i in range(len(filter_parts)):
                        if filter_parts[i] != '*' and filter_parts[i] != host_parts[i]:
                            match = False
                            break
                    if match:
                        flow.response = http.Response.make(404)
                        ctx.log.info(f"Blocked {host}")
                        return
            else:
                # Handle exact match filters
                if filter == host:
                    flow.response = http.Response.make(404)
                    ctx.log.info(f"Blocked {host}")
                    return

addons = [
    Blocker()
]
