class CityList():
    list = {}

    def add_item(self, city='', state='', craigslist_alias=''):
        self.list[city] = {'state':state, 'craigslist':craigslist_alias}