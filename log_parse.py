import sys
import re
import time
from urllib.parse import urlparse
from collections import Counter, defaultdict

def to_time(str_time):
	return time.strptime(str_time, '%d/%b/%Y %H:%M:%S')

def parse(
	ignore_files=False,
	ignore_urls=[],
	start_at=None,
	stop_at=None,
	request_type=None,
	ignore_www=False,
	slow_queries=False
):
	f = open('log.log', 'r')
	d1 = defaultdict(int)
	d2 = defaultdict(int)
	d_lists = defaultdict(list)
	
	to_return = []
	
	for line in f:        # *
		date_str = re.match('\[\d+/.*\]', line)
		if date_str:
		
			date = to_time(date_str.group(0).strip('[]'))
			if ((start_at and date < to_time(start_at)) or (stop_at and date > to_time(stop_at))):
				continue   # to*
			
			request = (re.search('\".*?\"', line).group(0)).strip('"').split()
			_req_type = request[0]
			url = request[1]

			if (_req_type == request_type) or (request_type is None): 									  #request_type
				
				o = urlparse(url)
				url = o.netloc + o.path
				
				if not(ignore_files) or (ignore_files and (re.search('\.\w+$', url) is None)):			  #ignore_files
					if not(url in ignore_urls):															  #ignore_urls

							if ignore_www:																  #ignore_www
								url = re.sub('w{3}\.', '', url)

							d1[url] +=1
							
							if slow_queries:
								req_time = int(re.search('\d+$', line).group(0))
								d2[url] += req_time
															
	if slow_queries:
		c = list(d1.items()) + list(d2.items())
		for u, t in c:
			d_lists[u].append(t)
		for ur in d_lists:
			d1[ur] = d_lists[ur][1]//d_lists[ur][0]
	
	for i in Counter(d1).most_common(5):
		to_return.append(i[1])
	
	f.close()
	return to_return


def main():
	print(parse())
	
if __name__ == "__main__":
	main()