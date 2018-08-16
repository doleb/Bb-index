from example.items import City

class CityList():
    list = {}

    def add_item(self, data, city='', state='', craigslist_alias=''):
        self.list[city] = {'item':data, 'state':state, 'craigslist':craigslist_alias}