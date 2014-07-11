#!/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

class GeoName:
  def __init__(self, _geonameid, _name, _alternatenames, _latitude, _longitude, _class_code, _feature_code, _country, _population, _elevation, _wikipedia_url, _entity_type):
    self.geonameid = _geonameid
    self.entity_type = _entity_type
    self.name = _name
    self.alternatenames = _alternatenames
    self.latitude = _latitude
    self.longitude = _longitude
    self.class_code = _class_code
    self.feature_code = _feature_code
    self.country = _country
    self.population = _population
    self.elevation = _elevation
    self.wikipedia_url = _wikipedia_url

  def __str__(self):
    return self.geonameid+"\t"+self.entity_type+"\t"+self.name+"\t"+"|".join(map(str, self.alternatenames))+"\t"+self.latitude+"\t"+self.longitude+"\t"+self.feature_code+"\t"+self.country+"\t"+self.population+"\t"+self.elevation+"\t"+self.wikipedia_url + "\t" + self.class_code
