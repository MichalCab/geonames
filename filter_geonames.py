#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import argparse
import urllib
import json
from multiprocessing import Pool

from src.binary_search import *
from src.load_file import *
from src.data_model import *
from src.remove_redirections import *
from src.remove_wiki_url_duplicities import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_country_codes = []
global_alternative_names = []
global_links = []
global_wikipedia_url_list = []
global_duplicate_urls = []
global_wikipedia_statistic = []
global_country_codes = []
subcountry_code = []

path = "/mnt/minerva1/nlp/projects/decipher_geonames/"
global_file_alternate_english_names = path + "help/alternate_english_names"
global_file_link = path + "help/links"
global_file_country_codes = path + "help/country_codes"
global_file_wikipedia_statistics = path + "help/wikipedia_statistics-final"
global_file_admin1_codes_ascii = path + "help/admin1_codes_ascii"
global_allowed_url = "http://en.wikipedia.org/wiki/"

global_S_wanted_freature_codes = ["CSTL", "HSTS", "MNMT", "PAL", "BDG", "BDGQ", "CH", "FT", "MSTY", "MUS", "OPRA", "PYR", "PYRS", "RLG"]

data_type = ""

def get_wikipedia_url(_wikipedia_url):
  result = ""
  #_wikipedia_url = _wikipedia_url.replace("$","\u")
  #_wikipedia_url = json.loads('"{0}"'.format(_wikipedia_url)).encode("utf-8")
  if _wikipedia_url:
    result = urllib.unquote(_wikipedia_url)
  return result

def load_alternative_names():
  f = open(global_file_alternate_english_names, "r")
  for r in f:
    global_alternative_names.append(r.strip().lower())

def load_links():
  f = open(global_file_link, "r")
  for r in f:
    global_links.append(r.strip())

def print_knowledge_base(_geonames):
  for g in _geonames:
    print g

def print_list(_geonames):
  for g in _geonames:
    if g.name not in g.alternatenames:
      print str(g.name) + "\t" + g.geonameid
    for t in g.alternatenames:
      print str(t) + "\t" + g.geonameid

def convert_input_to_knowledge_base_format(input_data):
  geonames_part = []
  for l in input_data:
    fields = l.strip().split("\t")

    geonameid = fields[0]
    population = fields[14]

    wikipedia_url = -1

    #dont touch this, its crazy :( but works :)
    if not ((fields[6] is not "S" or ( fields[6] is "S" 
            and fields[7] in global_S_wanted_freature_codes)) 
            and (((data_type == "location" and fields[7] != "MUS")
          or(data_type == "museum" and (fields[7] == "MUS") 
            or data_type == "all")))):
        continue
  
    # WIKIPEDIA URL
    wikipedia_url_all_occur = binary_search_all_occur(
        global_links, geonameid, cross_columns=True, col_sep="\t", 
        finding_column=0, return_column=1)

    if len(wikipedia_url_all_occur) is 0:
      continue

    # vybere lépe ohodnocenou url ze souboru links z geonames na základě 
    # wikipedia statistik (např. Istanbul místo Constantinopole)
    maxscore = -1
    go_next = False
    if len(wikipedia_url_all_occur) > 1:
      for url in wikipedia_url_all_occur:
        if global_allowed_url not in url:
          go_next = True
          continue
        url = get_wikipedia_url(url)
        score = binary_search(
            global_wikipedia_statistic, url.replace(global_allowed_url, ""),
            cross_columns=True, col_sep="\t", finding_column=0, 
            return_column=2)

        if int(score) > int(maxscore):
          maxscore = score
          wikipedia_url = url

    if go_next:
      continue

    if maxscore is -1:
      wikipedia_url = wikipedia_url_all_occur[0]
    wikipedia_url = urllib.unquote(wikipedia_url)

    entity_type = "museum" if "museum" == data_type else "location"

    name = fields[1]

    #alternative names
    names = fields[3].split(",")
    alternatenames = set()

    for n in names:
      n = n.strip()
      if n and n.lower() in global_alternative_names:
        alternatenames.add(n)

    state = binary_search(
        global_country_codes, fields[8], cross_columns=True, col_sep="\t", 
        finding_column=0, return_column=1)

    if state is not -1 and state:
      alternatenames.add(name + ", " + state)
      country = state
    else:
      country = ""

    # substate (USA states)
    if fields[10]:
      substate = binary_search(
          subcountry_code, fields[8] + "." + fields[10], cross_columns=True, 
          col_sep="\t", finding_column=0, return_column=1)
      if substate is not -1 and substate:
        alternatenames.add(name + ", " + substate)

    latitude = fields[4]
    longitude = fields[5]
    class_code = fields[6]
    feature_code = fields[7]
    elevation = fields[15]

    new_geoname = GeoName(
        geonameid, name, alternatenames, latitude,
        longitude, class_code, feature_code, country, 
        population, elevation, wikipedia_url, entity_type)

    geonames_part.append(new_geoname)
  return geonames_part

def split_list(alist, wanted_parts=1):
  length = len(alist)
  return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
    for i in range(wanted_parts) ]

if  __name__ == "__main__":
  load_alternative_names()
  global_country_codes = load_file(global_file_country_codes)
  global_country_codes.sort()

  subcountry_code = load_file(global_file_admin1_codes_ascii)
  subcountry_code.sort()

  load_links()
  global_links.sort()

  global_wikipedia_statistic = load_file(global_file_wikipedia_statistics)
  global_wikipedia_statistic.sort()

  # argument parsing
  parser = argparse.ArgumentParser()
  parser.add_argument('-l', '--list', action='store_true', default=False,
                      dest='list', help='Print list for an automaton.')
  parser.add_argument('-t', '--data-type', default=False, dest='data_type', 
                      type=str, help='Select data type to convert.', 
                      nargs=1)
  parser.add_argument('-b', '--print-knowledge-base', action='store_true',
                      default=False, dest='print_knowledge_base', 
                      help='Print knowledge base.')
  arguments = parser.parse_args()

  if ((not arguments.data_type) or
        (arguments.data_type and
        arguments.data_type[0] != "location" and
        arguments.data_type[0] != "locations" and
        arguments.data_type[0] != "museum" and
        arguments.data_type[0] != "museums" and
        arguments.data_type[0] != "all")):
    parser.error('No action requested, add -t <location(s)|museum(s)|all>')

  # resolve data_type
  if "museum" in arguments.data_type[0]:
    data_type = "museum"
  elif "location" in arguments.data_type[0]:
    data_type = "location"
  else:
    data_type = "all"
  
  input_data = sys.stdin.read().splitlines()

  geonames = []
  if input_data > 50000:
    # run 6 process for convert input to knowledge_base format
    num_of_subprocess = 6
    chunks = split_list(input_data, wanted_parts=num_of_subprocess)
    pool = Pool(num_of_subprocess)
    results = []
    t = pool.map_async(convert_input_to_knowledge_base_format, chunks, callback=results.extend)
    t.wait()

    # merge results
    for r in results:
      geonames.extend(r)
  else:
    geonames = convert_input_to_knowledge_base_format(input_data)

  if len(geonames) > 0:
    geonames = remove_redirections(geonames)
    
    # find url duplicities
    for g in geonames:
      if g.wikipedia_url in global_wikipedia_url_list:
        global_duplicate_urls.append(g.wikipedia_url)
      global_wikipedia_url_list.append(g.wikipedia_url)

    # remove url duplicities
    geonames = remove_wiki_url_duplicities(geonames, global_duplicate_urls)
  
  # print data
  if arguments.list:
    print_list(geonames)
  if arguments.print_knowledge_base:
    print_knowledge_base(geonames)
