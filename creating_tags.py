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

# Define a starting post ID and starting tag ID
count = 10
tag_count = 10
# ---------------------------------

# parsing title and name
def get_title(filename):
	filename = filename.strip()
	filename = filename.replace("\xcc","").replace("\x81","")
	post_title = filename.replace(".txt","")
	return post_title

# Return 3 tags
def find_tags(post_title, post_content):
	tags = post_content.replace(",","").split(" ")
	return [post_title.split(" ")[-1].split(".")[-1], tags[0], tags[1]]

# Create wp_terms, wp_term_taxonomy, wp_term_relationships
def create_wp_terms_taxonomy(term_id, tag, object_id):
	name=tag
	slug=name
	term_taxonomy_id=term_id
	parent=0
	count=1
	taxonomy="post_tag"
	description=""
	term_order=0
	term_group=0

	wp_terms={"term_id":term_id, 
			  "name":name, 
			  "slug":slug, 
			  "term_group":term_group}

	wp_term_taxonomy={"term_taxonomy_id":term_taxonomy_id, 
					  "term_id":term_id, 
					  "taxonomy":taxonomy, 
					  "description":description, 
					  "parent":parent, 
					  "count":count}

	wp_term_relationships={"object_id":object_id, 
						   "term_taxonomy_id":term_taxonomy_id, 
						   "term_order":term_order}

	return [wp_terms, wp_term_taxonomy, wp_term_relationships]

# Function to write on the files
def save_file(filename, fieldname, array):
	with open(filename, "wb") as csvfile:
		writer = csv.DictWriter(csvfile, delimiter=',', fieldnames = fieldname)
		for item in array:
			writer.writerow(item)

# Collect files from local directory
files = os.listdir(file_path)
if '.DS_Store' in files:
	files = files[1:]
object_id = count
term_id = tag_count
terms = []
taxonomy = []
relationships = []

for filename in files:

	with open("{}/{}".format(file_path, filename)) as F:
		post_content = ""
		for line in F:
			post_content += line.strip()
			break

	post_title = get_title(filename)
	tags = find_tags(post_title, post_content)

	for tag in tags:
		wp_terms, wp_term_taxonomy, wp_term_relationships = create_wp_terms_taxonomy(term_id, tag, object_id)
		terms.append(wp_terms)
		taxonomy.append(wp_term_taxonomy)
		relationships.append(wp_term_relationships)
		term_id += 1

	object_id += 1

fieldname = ['term_id', 'name', 'slug', 'term_group']
save_file("import_to_wp_terms.csv", fieldname, terms)

fieldname = ['term_taxonomy_id', 'term_id', 'taxonomy', 'description', 'parent', 'count']
save_file("import_to_wp_term_taxonomy.csv", fieldname, taxonomy)

fieldname = ['object_id', 'term_taxonomy_id', 'term_order']
save_file("import_to_wp_term_relationships.csv", fieldname, relationships)
