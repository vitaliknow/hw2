import sys
import re
import time
from urllib.parse import urlparse
from collections import Counter

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
	dict = {}
	to_return = []
	
	for line in f:        # *
		date_str = re.match('\[\d+/.*\]', line)
		if date_str is not None:
		
			date = to_time(date_str.group(0).strip('[]'))
			if (((start_at is not None) and date < to_time(start_at)) or ((stop_at is not None) and date > to_time(stop_at))):
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
								url = re.sub('w{3}.', '', url)
								
							if slow_queries:
								req_time = int(re.search('\d+$', line).group(0))
								
							if dict.get(url) is None:
								if slow_queries:
									dict[url] = [1, req_time]
								else:
									dict[url] = 1
							else:
								if slow_queries:															
									dict[url][0] +=	1
									dict[url][1] += req_time
								else:
									dict[url] += 1
	if slow_queries:
		for u in dict:
			dict[u] = dict[u][1]//dict[u][0]
	
	for i in Counter(dict).most_common(5):
		to_return.append(i[1])
	
	f.close()
	return to_return



def main():
	print(parse())
	
if __name__ == "__main__":
	main()