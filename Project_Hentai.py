#!/usr/bin/env python3.7

import sys
import re
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
driver.implicitly_wait(10)
driver.get('https://www.projecthentai.com')
frames = driver.find_elements_by_tag_name('iframe')
for frame in frames:
	driver.switch_to.default_content()
	driver.switch_to.frame(frame)
	try:
		search_elem = driver.find_element_by_class_name('ecwid-search-widget__input')
		search.elem = send_keys(author, Keys.ENTER)
		break
	except NoSuchElementException:
		continue

# TODO Now we should be at the search results page

driver.switch_to.default_content()

res_count_elem = driver.find_element_by_class_name('pager__count-pages')

# TODO get element text

res_count = int(re.search(r"of (\d+) items", res_count_elem_text).group(1))

# TODO What is this? params += '&offset=60'

# TODO what? url = driver.getCurrentUrl()
