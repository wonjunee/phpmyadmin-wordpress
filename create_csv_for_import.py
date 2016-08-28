# -*- coding: utf8 -*-
import json
import csv
from pprint import pprint
import datetime as dt
import os

# ---------------------------------
#            INPUT
# ---------------------------------
# Define file path
file_path = "./files_small"

# Define a starting ID #
count = 10
# ---------------------------------

# Function to create a post dictionary
def create_post(post_id, post_content, post_title, post_name):
	post_date = "{:%Y-%m-%d %H:%M:%S}".format(dt.datetime.now())
	post = {'ID': post_id,
			'post_author': u'1',
			'post_date': post_date,
		    'post_date_gmt': post_date,
		    'post_content': post_content,
		    'post_title': post_title,
		    'post_excerpt': u'',
		    'post_status': u'publish',
		    'comment_status': u'open',
		    'ping_status': u'open',
		    'post_password': u'',
		    'post_name': post_name,
		    'to_ping': u'',
		    'pinged': u'',
		    'post_modified': post_date,
		    'post_modified_gmt': post_date,
		    'post_content_filtered': u'',
		    'post_parent': u'0',
		    'guid': 'http://localhost/wp/?p={}'.format(post_id),
		    'menu_order': u'0',
		    'post_type': u'post',
		    'post_mime_type': u'',
		    'comment_count': u'0'}
		    
	return post

# parsing title and name
def get_title_name(filename):
	filename = filename.strip()
	filename = filename.replace("\xcc","").replace("\x81","")
	post_title = filename.replace(".txt","")
	post_name = post_title.replace(" ","").replace(",","")
	return post_title, post_name


files = os.listdir(file_path)
if '.DS_Store' in files:
	files = files[1:]

with open("import_to_phpmyadmin.csv", "w") as csvfile:
	fieldname = ['ID',
				'post_author',
				'post_date',
			    'post_date_gmt',
			    'post_content',
			    'post_title',
			    'post_excerpt',
			    'post_status',
			    'comment_status',
			    'ping_status',
			    'post_password',
			    'post_name',
			    'to_ping',
			    'pinged',
			    'post_modified',
			    'post_modified_gmt',
			    'post_content_filtered',
			    'post_parent',
			    'guid',
			    'menu_order',
			    'post_type',
			    'post_mime_type',
			    'comment_count']
	writer = csv.DictWriter(csvfile, delimiter=',', fieldnames = fieldname)

	for filename in files:
		with open("{}/{}".format(file_path, filename)) as F:
			post_content = ""
			for line in F:
				post_content += line.strip()+"\n"
		post_title, post_name = get_title_name(filename)
		post_id = count
		writer.writerow(create_post(post_id, post_content, post_title, post_name))
		count+=1
	print count

