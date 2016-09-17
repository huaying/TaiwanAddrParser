# -- coding: UTF-8 --
import json, collections, re
import urllib.request

class TaiwanAddrParser:

    taiwan = None
    cities = {}
    areas = collections.defaultdict(list)
    valid_addr = set()

    def __init__(self):
        self.load()
        self.buildIndex()
    def load(self):
        with open('parsers/TaiwanAddress.json') as json_file:
            self.taiwan = json.load(json_file)

    def buildIndex(self):
        for city in self.taiwan:
            cityname = city['CityName']
            self.cities[cityname.replace(u'臺',u'台')] = city
            self.cities[cityname] = city
            for area in city['AreaList']:
                self.areas[area['AreaName']].append(cityname)


    def parse(self, source_file, isUrl=True):
        print(source_file )
        onetime_result = set()

        if isUrl:
            source = urllib.request.urlopen(source_file)
        else:
            source = open(source_file)
                   
        with source as input_file:
            for line in input_file:
                try:
                    line = line.strip().decode('utf-8')
                except: pass
                n = len(line)
                for i in range(n):
                    if line[i:i+3] in self.cities:
                        end = re.search(r"\W",line[i:]).start()
                        addr = line[i:i+end]
                        if end > 3 and self.validateAddr(addr): 
                            onetime_result.add(addr)
        return json.dumps(list(onetime_result))

    def validateAddr(self,addr):
        googleapi = "http://maps.googleapis.com/maps/api/geocode/json?address="
        geocode = urllib.request.urlopen(googleapi+urllib.parse.quote(addr))
        res = json.loads(geocode.read().decode('utf-8'))
    
        if res and res["results"]:
            rlt = res["results"][0]
            if rlt["geometry"]["location_type"] != "APPROXIMATE" and "Taiwan" in rlt["formatted_address"]:
                return True
        return False

tap = TaiwanAddrParser()

if __name__ == "__main__":
    tap.parse("http://money9992.pixnet.net/blog/post/452133488")
    tap.parse("https://tw.ysm.emarketing.yahoo.com/soeasy/?fe_type=1",True)
    print(tap.valid_addr)
