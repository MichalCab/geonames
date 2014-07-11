#!/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

def binary_search(a, x, lo=0, hi=None, cross_columns=False, col_sep=" ", finding_column=0, return_column=1):
  if hi is None:
    hi = len(a)
  while lo < hi:
    mid = (lo+hi)//2
    midval = a[mid]
    if cross_columns:
      splited_line = midval.split(col_sep)
      midval = splited_line[finding_column].replace("\t", "").replace("\n", "")
      #print ":%s:%s:" % (midval, x)
    if midval < x:
      lo = mid + 1
    elif midval > x:
      hi = mid
    else:
      if cross_columns:
        return splited_line[return_column]
      return mid
  return -1

def binary_search_all_occur(a, x, lo=0, hi=None, cross_columns=False, col_sep=" ", finding_column=0, return_column=1):
  results = set()
  part_results1 = []
  part_results2 = []
  # find left most
  if hi is None:
    hi = len(a)
  while lo < hi:
    mid = (lo+hi)//2
    midval = a[mid]
    if cross_columns:
      splited_line = midval.split(col_sep)
      midval = splited_line[finding_column].replace("\t", "").replace("\n", "")
    if x > midval:
      lo = mid + 1
    elif x < midval:
      hi = mid
    else:
      if cross_columns:
        part_results1.append(splited_line[return_column])
      else:
        part_results1.append(mid)
      hi = mid
  results.update(part_results1)
  lo = 0
  hi = len(a)
  # find right most
  while lo < hi:
    mid = (lo+hi)//2
    midval = a[mid]
    if cross_columns:
      splited_line = midval.split(col_sep)
      midval = splited_line[finding_column].replace("\t", "").replace("\n", "")
    if x > midval:
      lo = mid + 1
    elif x < midval:
      hi = mid
    else:
      if cross_columns:
        part_results2.append(splited_line[return_column])
      else:
        part_results2.append(mid)
      lo = mid + 1
  results.update(part_results2)
  return list(results)
