import scrapy
from example.file_utils import CITY_LIST
from example.items import City



#gathers census data for individual cities and determines the "diversity" of a given city based on the distribution of a population across ethnic groups
#Groups as determined by City-Data.com are White, Black, Hispanic, Asian, Native American, Native Hawaiian/Pacific Islander, 2+ Races, and Other 
class DiversityCrawler(scrapy.Spider):
    name = 'diversitycrawler'
    allowed_domains = ['citydata.com']
    start_urls = []
    city_iter = iter(CITY_LIST)

    def __init__(self):
        for line in CITY_LIST:
            dashed = line.replace(' ', '-').strip()
            if 'DC' in line:
                dashed = 'Washington-District-of-Columbia'
            self.start_urls.append('http://www.city-data.com/city/%s.html' % dashed)

    #extracts the percentage of each race within a city's population from response page
    def parse(self, response):
        percentages = []
        pop_list = response.xpath('//*[@id="races-graph"]/div/ul/li[2]/ul/li/span[2]/text()').extract()#list of population distribution %
        race_names = response.xpath('//*[@id="races-graph"]/div/ul/li[2]/ul/li/b/text()').extract()
        for percent in pop_list:
            percentages.append(float(percent.rstrip('%')))
        yield self.make_item(response, percentages, race_names)

    #places extracted information into items 
    def make_item(self, response, percentages, races):
        item = City()
        try:
            city = next(self.city_iter)
        except Exception as ex:
            print('end of list')
        item['name'] = city
        for i in range(len(percentages)):
            race = str(races[i]).split(' ')[0].lower()
            percent = percentages[i]
            if race == 'native':
                race = 'pacific'
            elif race == 'two':
                race = 'other'
            item[race] = percent
            
        return item

    #calculates overall diversity score for a cities population and returns score and largest demographic
    def calculate_diversity(self, percentages, races):
        largest_demographic = ''
        largest_percentage = 0.0
        for i in range(len(percentages)):
            if percentages[i] > largest_percentage:
                largest_demographic = races[i]
                largest_percentage = percentages[i]
        baseIndex = ((100.0/(len(percentages)-2))/largest_percentage)*100.0
        if largest_demographic == 'White only':
            baseIndex *= 0.5
        elif largest_demographic == 'Hispanic':
            baseIndex *= 1.5
        elif largest_demographic == 'Black only':
            baseIndex *= 1.5
        elif largest_demographic == 'Asian only':
            baseIndex *= 1.5
        return [round(baseIndex, 2), largest_demographic]
        