#!/bin/env python
#-*- coding: utf-8 -*-

import fileinput
import urllib
import os
import os.path
import sys
import getopt
import json
import argparse
import gzip
import time
import urllib
from multiprocessing import Pool

from binary_search import binary_search
from load_file import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_file_with_redirection = "help/wikipedia-redirects.tsv"

redirections = []
redirections0 = []
original_redirections = []

def split_list(alist, wanted_parts=1):
  length = len(alist)
  return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
    for i in range(wanted_parts) ]

def prepare_help_files():
  original_redirections = load_file(global_file_with_redirection)
  for r in original_redirections:
    red_array = r.split("\t")
    redirection_names = red_array[1].split("|")
    for rn in redirection_names:
      redirections.append("%s\t%s" % (rn.strip(), red_array[0]))
      redirections.append("%s\t%s" % (rn.strip().lower(), red_array[0]))
      redirections0.append(red_array[0])

  redirections0.sort()
  redirections.sort()
  original_redirections[:] = []

def remove_redirections(geonames):
  prepare_help_files()
  
  if len(geonames) > 50000:
    num_of_subprocess = 6
    chunks = split_list(geonames, wanted_parts=num_of_subprocess)
    pool = Pool(num_of_subprocess)

    results = []
    t = pool.map_async(remove_redirection_part, chunks, callback=results.extend)
    t.wait()

    chunks = []
    for r in results:
      chunks.extend(r)

    final = []
    for ch in chunks:
      final.append(ch)
  else:
    final = remove_redirection_part(geonames)
  return final
  
def remove_redirection_part(geonames):
  for g in geonames:
    not_redirection = binary_search(redirections0, g.wikipedia_url)
    if not_redirection is -1:
      wiki_key = g.wikipedia_url.replace("http://en.wikipedia.org/wiki/", "").replace("_", " ")
      final_url = binary_search(redirections, wiki_key, cross_columns=True, col_sep="\t", finding_column=0, return_column=1)
      if final_url is not -1:
        g.wikipedia_url = final_url
      else:
        wiki_key = wiki_key.lower()
        final_url = binary_search(redirections, wiki_key, cross_columns=True, col_sep="\t", finding_column=0, return_column=1)
        if final_url is not -1:
          g.wikipedia_url = final_url
  return geonames
