import requests, time
from lxml import etree

class BBSListFetcher(object):
	def __init__(self):
		self._host      = None
		self._board     = None
		self._previous  = None
		self._criteria  = None
		self._delay     = 3
		self._linktable = {}

	def _update_previous_page(self, content):
		html   = etree.HTML(content)
		result = html.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href')

		self._previous = result[0]

	def _update_link_table(self, content):
		html = etree.HTML(content)
		lst_etree_title_object = html.xpath('//*[@id="main-container"]/div[2]/div[@class="r-ent"]')
		for etree_title_object in lst_etree_title_object:
			count = 0
			url   = None
			title = None

			res_count = etree_title_object.xpath('.//div[@class="nrec"]/span')
			if res_count:
				try:
					count = int(res_count[0].text)
				except:
					count = 101
					
			res_url   = etree_title_object.xpath('.//div[@class="title"]/a/@href')
			res_title = etree_title_object.xpath('.//div[@class="title"]/a')
			if res_url:
				url = res_url[0]
				title = res_title[0].text

			if url and self._criteria and count >= self._criteria:
				self._linktable['%s/%s'%(self._host, url)] = title

	def _this_page(self, next_page = None):
		str_target_url = '%s/bbs/%s/index.html'%(self._host, self._board.lower())
		if next_page:
			str_target_url = '%s/%s'%(self._host, next_page)

		res = requests.get(str_target_url)
		str_content = res.text

		self._update_previous_page(str_content)
		self._update_link_table(str_content)

	def set_target(self, host = None, board = None, criteria = None, delay = None):
		if host:
			self._host = host
		if board:
			self._board = board
		if criteria:
			self._criteria = criteria
		if delay:
			self._delay = delay

	def get_list(self, pages=3):
		# get link table
		if self._host and self._board:
			next_page = None
			for now_run in range(0, pages):
				self._this_page(next_page)
		else:
			raise BaseException('Miss host or board')

		return self._linktable

def get_images_in_page(url):
	res    = requests.get(url)
	html   = etree.HTML(res.text)
	interest_ext = ['jpg','png']

	lst_etree_link_object  = html.xpath('//*[@id="main-content"]/a/@href')

	for link in lst_etree_link_object:
		for ext in interest_ext:
			if ext in link.lower()[-3:]:
				print(link)



