#!/usr/bin/env python3.7

import sys
import re
from itertools import count
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

if len(sys.argv) != 2:
	print('usage: python3 Project_Hentai.py "author name"')
	exit(1)
author = sys.argv[1]

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

def build_url(query, page):
	if page == 1:
		return ('https://www.projecthentai.com/online-store/hex%3A' + 
		  f'search?keyword={query}'.encode().hex())
	else:
		return ('https://www.projecthentai.com/online-store/hex%3A' +
		  f'search?keyword={query}&offset={(page - 1) * 60}'.encode().hex())

def switch_to_results_frame():
	driver.switch_to.default_content()
	frames = driver.find_elements_by_tag_name('iframe')
	for frame in frames:
			driver.switch_to.default_content()
			driver.switch_to.frame(frame)
			try:
				search_elem = driver.find_element_by_class_name(
					'ecwid-productBrowser-SearchPage')
				return True
			except NoSuchElementException:
				pass
	return False

for page in count(1):
	driver.switch_to.default_content()
	driver.get(build_url(author, page))
	for attempt in range(20):
		if switch_to_results_frame():
			break
		else:
			sleep(0.5)
	else:
		print('products iframe not found', file=sys.stderr)
		exit(1)

	for attempt in range(20):
		try:
			try:
				driver.find_element_by_class_name('search__notice')
				exit(0)
			except NoSuchElementException:
				pass
			driver.find_element_by_class_name('grid-product__title-inner')
			break
		except NoSuchElementException:
			sleep(0.5)
	else:
		print('no results found', file=sys.stderr)
		exit(0)
	prods = driver.find_elements_by_class_name('grid-product__title-inner')
	for product in prods:
		print(product.get_attribute('innerHTML'))
	try:
		res_count_elem = driver.find_element_by_class_name(
				'pager__count-pages')
	except:
		break
	res_count_elem_text = res_count_elem.get_attribute('innerHTML')
	res_count = int(re.search(r"of (\d+) items", res_count_elem_text).group(1))
	if page * 60 >= res_count:
		break	
