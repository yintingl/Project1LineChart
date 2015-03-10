#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import csv
from webapp2_extras import jinja2
from webapp2_extras import json
import logging


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
		rv = self.jinja2.render_template(_template, **context)
		self.response.write(rv)

class MainHandler(BaseHandler):
    def get(self):
             data = self.data_passer()
             logging.info(data)
             context = {'data':data[0],'data2':data[1]}
             self.render_response('index.html', **context)

    def data_passer(self): # decides which data to pass to client
		# create data object containing all year information
               	final_result=[]
		data = {"2006":[],"2007":[],"2008":[],"2009":[],"2010":[],"2011":[],"2012":[],"2013":[]}
		for year in data:
			data[year] = self.get_year_data(year)
		years = ["2006","2007","2008","2009","2010","2011","2012","2013"]
		#passing = {}
		index=6
		#la = ["Education"]
		#passing["labels"]=years
                se = []
		
               	activity_day= self.get_data_for_activity(data,index,years,"Percent Engaged on Weekdays",True)
                #passing["Activity"]=activity_day[0]
                for i in range (0, len(activity_day[1])):
                        temp_dict={}
                    	temp_dict["Activity"]=activity_day[0]
                        temp_dict["Year"]=years[i]
                	temp_dict["Percentage"]=float(activity_day[1][i])
                    	#temp_day=float(activity_day[1][i])
                        
                        #temp_list_day.append(temp_day)
                        
                        se.append(temp_dict)
                #passing["series"]=se
                final_result.append(se)
            
                sub = []
                activit_sub = self.get_data_for_activity(data,index,years,"Sub-Activities",True)
                for i in range (0, len(activit_sub[1])):
                    	temp_dict = {}
                        temp_dict["Activity"]=activit_sub[1][i][0]["Activity"]
                    	temp_dict["Year"]=years[i]
                        temp_dict["Percentage"]=float(activit_sub[1][i][0]["Percent Engaged on Weekdays"])
                   	sub.append(temp_dict)
            	final_result.append(sub)
           
  #{"title":"Personal Care","subtitle":"Time, in hours","ranges":[6,9,12],"measures":[8.99,9.92],"markers":[8]},
  #{"title":"Household","subtitle":"Time, in hours","ranges":[1,2,4],"measures":[1.95,2.56],"markers":[2]},
  #{"title":"Working","subtitle":"Time, in hours","ranges":[4,8,12],"measures":[8.57,5.92],"markers":[7]},
  #{"title":"Educational","subtitle":"Time, in hours","ranges":[2,6,10],"measures":[6.46,3.21],"markers":[3]},
  #{"title":"Leisure & Sports","subtitle":"Time, in hours","ranges":[3.5,5.25,9],"measures":[5.23,7.13],"markers":[5]}

		return final_result
     
    def get_data_for_activity(self,data,index,years,key,sub_activity):
		# TODO: figure out how to recurse through this
		d = []
		for year in years:
			#info = {}
			#info["year"] = year
			#info[data[years[0]][index]["Activity"]] = data[year][index][key]
			value=data[year][index][key]
			d.append(value)
		return [data[years[0]][index]["Activity"], d]
		#return info;
    def get_year_data(self,year): 
		# Note: '#' char in csv strings is a stand-in for a comma
		# What to do with negative time values?
		f = open('data/{0}.csv'.format(year))
		j = []
		headers = ["Activity","Percent Engaged on Weekdays","Percent Engaged on Weekends and Holidays",
		"Average Hours per Weekday","Average Hours per Weekend and Holiday"]
		reader = csv.DictReader(f, headers)
		# logging.info(reader)
		for row in reader:
			j.append(row)
		k = []
		# Personal care activities
		act = j[0]
		act["Sub-Activities"] = j[1:6]
		k.append(act)
		# Eating and drinking
		act = j[6]
		act["Sub-Activities"] = j[7:9]
		k.append(act)
		# Household activities
		act = j[9]
		act["Sub-Activities"] = j[10:20]
		k.append(act)
		# Purchasing goods and services
		act = j[20]
		act["Sub-Activities"] = []
		# Consumer goods purchases
		s_act = j[21]
		s_act["Sub-Activities"] = j[22]
		act["Sub-Activities"].append(s_act)
		# Professional and personal care services
		s_act = j[23]
		s_act["Sub-Activities"] = j[24:27]
		act["Sub-Activities"].append(s_act)
		# Household services
		s_act = j[27]
		s_act["Sub-Activities"] = j[28:30]
		act["Sub-Activities"].append(s_act)
		act["Sub-Activities"].append(j[30])
		act["Sub-Activities"].append(j[31])
		k.append(act)
		# Caring for and helping others
		act = j[32]
		act["Sub-Activities"] = []
		s_act = j[33]
		s_act["Sub-Activities"] = j[34:37]
		act["Sub-Activities"].append(s_act)
		s_act = j[37]
		s_act["Sub-Activities"] = j[38:40]
		act["Sub-Activities"].append(s_act)
		act["Sub-Activities"].append(j[40])
		act["Sub-Activities"].append(j[41])
		s_act = j[42]
		s_act["Sub-Activities"] = [j[43:45]]
		act["Sub-Activities"].append(s_act)
		act["Sub-Activities"].append(j[45])
		k.append(act)
		# Work and work-related activities
		act = j[46]
		act["Sub-Activities"] = j[47:52]
		k.append(act)
		# Educational activities
		act = j[52]
		act["Sub-Activities"] = j[53:56]
		k.append(act)
		# Organizational, civic, and religious activities
		act = j[56]
		act["Sub-Activities"] = [j[57]]
		s_act = j[58]
		s_act["Sub-Activities"] = []
		s_s_act = j[59]
		s_s_act["Sub-Activities"] = j[60:65]
		s_act["Sub-Activities"].append(s_s_act)
		s_act["Sub-Activities"].append(j[65])
		act["Sub-Activities"].append(s_act)
		act["Sub-Activities"].append(j[66])
		k.append(act)
		# Leisure and sports
		act = j[67]
		act["Sub-Activities"] = []
		s_act = j[68]
		s_s_act = j[69]
		s_s_act["Sub-Activities"] = j[70:72]
		s_act["Sub-Activities"] = [s_s_act]
		s_s_act = j[72]
		s_s_act["Sub-Activities"] = [j[73]]
		s_act["Sub-Activities"].append(s_s_act)
		s_act["Sub-Activities"].append(j[74])
		act["Sub-Activities"].append(s_act)
		s_act = j[75]
		s_act["Sub-Activities"] = j[76:78]
		act["Sub-Activities"].append(s_act)
		act["Sub-Activities"].append(j[78])
		k.append(act)
		# Telephone calls, mail, and emails
		act = j[79]
		act["Sub-Activities"] = [j[80]]
		s_act = j[81]
		s_act["Sub-Activities"] = j[82:84]
		act["Sub-Activities"].append(s_act)
		act["Sub-Activities"].append(j[84])
		k.append(act)
		# Other activities, not elsewhere classified
		k.append(j[85])
		return k
    def post(self):
		context = {}
		self.render_response('index.html', **context)

app = webapp2.WSGIApplication([
    ('.*', MainHandler)
], debug=True)
