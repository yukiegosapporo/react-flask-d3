import requests
import os
import pandas as pd
import json
from datetime import datetime

gi = '0041500116'

def get_data(gi):
	URL = 'http://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID={gi}&RangeType=2&Season=2015-16&SeasonType=Playoffs&StartPeriod=1&StartRange=0'

	os.system('curl "{URL}" > game.json'.format(URL=URL.format(gi=gi)))

	raw = pd.DataFrame()
	with open("game.json") as json_file:
	        parsed = json.load(json_file)['resultSets'][0]
	        raw = raw.append(
	            pd.DataFrame(parsed['rowSet'], columns=parsed['headers']))
	raw['WCTIMESTRING'] = raw['WCTIMESTRING'].apply(
	    lambda x:datetime.strptime(x,'%I:%M %p'))

	raw["SCORE"] = raw["SCORE"].fillna(method="ffill").fillna("0 - 0 ")

	output = {'events':[]}
	sec = 0
	for index, row in raw.iterrows():
	    if (row.HOMEDESCRIPTION is not None) & (row.VISITORDESCRIPTION is
	       None):
	        output['events'].append(
	            {
	            'start_date':{'year':'2016',
	                'hour':row['WCTIMESTRING'].hour,
	                'minute':row['WCTIMESTRING'].minute,
	                'second':sec},
	            'text':{'headline':row['HOMEDESCRIPTION'],
	                'text':row['SCORE']}
	            })
	    elif (row.HOMEDESCRIPTION is not None) & (row.VISITORDESCRIPTION is
	       None):
	        output['events'].append(
	            {
	            'start_date':{'year':'2016',
	                'hour':row['WCTIMESTRING'].hour,
	                'minute':row['WCTIMESTRING'].minute,
	                'second':sec},
	            'text':{'headline':row['VISITORDESCRIPTION'],
	                'text':row['SCORE']}
	            })
	    elif (row.HOMEDESCRIPTION is not None) & (row.VISITORDESCRIPTION is not
	       None):
	        output['events'].append(
	            {
	            'start_date':{'year':'2016',
	                'hour':row['WCTIMESTRING'].hour,
	                'minute':row['WCTIMESTRING'].minute,
	                'second':sec},
	            'text':{'headline':(row['HOMEDESCRIPTION'] + ' & ' +
	                row['VISITORDESCRIPTION']),
	                'text':row['SCORE']}
	            })
	    if index != raw.shape[0]-1:
	        if raw.ix[index,'WCTIMESTRING'] == raw.ix[index+1,'WCTIMESTRING']:
	            sec += 1
	        else:
	            sec = 0

	# output_json = json.dumps(output)
	return output

# URL2 = 'http://stats.nba.com/stats/videoevents?GameEventID={ei}&EndPeriod=10&EndRange=55800&GameID={gi}&RangeType=2&Season=2015-16&SeasonType=Playoffs&StartPeriod=1&StartRange=0'

# for ei in xrange(maxevent):
#     r = requests.get(URL2.format(ei=ei,gi=gi))
#     if r.status_code == 200:
#         print 'yes'
#     else:
#         print 'no'



# 'http://stats.nba.com/media/video/thumbs/20160429/57359553_14.jpg'