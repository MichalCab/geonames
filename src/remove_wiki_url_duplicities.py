#!/bin/env python
#-*- coding: utf-8 -*-
#file: remove_wiki_url_duplicities.py

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

def remove_wiki_url_duplicities(geonames, urls):
  geonames_without_dup = []
  duplicities = []
  for g in geonames:
    if g.wikipedia_url not in urls:
      geonames_without_dup.append(g)
      continue

    if "ADM" in g.feature_code:
      score = 0
    elif "PPL" in g.feature_code:
      score = 1
    else:
      score = 2
    subscore = len(str(g))
    new_dup = {'entity' : g, 'score' : score, 'subscore' : subscore}

    founded = False
    for d in duplicities:
      if str(d["url"]) == str(g.wikipedia_url):
        founded = True
        if new_dup['score'] > d['entry']['score'] or (new_dup['subscore'] > d['entry']['subscore'] and new_dup['score'] == d['entry']['score']):
          d['entry'] = new_dup

    if not founded:
      duplicities.append({'url': g.wikipedia_url, 'entry': {'entity' : g, 'score' : score, 'subscore' : subscore}})

  for d in duplicities:
    geonames_without_dup.append(d['entry']['entity'])

  return geonames_without_dup
