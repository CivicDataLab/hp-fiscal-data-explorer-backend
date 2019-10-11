# -*- coding: utf-8 -*-
import csv
import os
from urllib.parse import urlencode
import pdb
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError

from scraper.settings import DATASET_PATH
from scraper.utils import parsing_utils


class BudgetBaseSpider(scrapy.Spider):
    '''
    Base spider for HP budget. It has methods for making dataset requests
    for a given HOD code with a given query with given date.
    '''
    allowed_domains = ['himkosh.hp.nic.in']
    query_url = None
    unit = None

    def __init__(self, *args, **kwargs):
        super(BudgetBaseSpider, self).__init__(*args, **kwargs)
        if not hasattr(self, 'date'):
            raise CloseSpider('No date given!')
        
        self.date = kwargs.pop('date')
        self.query_id = kwargs.pop('query_id', None)
        self.query_name = kwargs.pop('query_name', None)
        self.hod_name = kwargs.pop('hod_name', None)
        
    def make_dataset_request(self, params):
        '''
        Construct and yield a scrapy request for a dataset.
        '''
        # generate a filepath to store the dataset in.
        filename = '{}_{}.csv'.format(self.name, self.date)

        filepath = os.path.join(DATASET_PATH, filename)

        # don't request the same dataset again if it's already collected previously
        # check if a file with a particular dataset name exist, if it does then
        # also check if it's empty or not, if it's empty we request it again.
        if not os.path.exists(filepath) or not os.stat(filepath).st_size:
            query_params = {
                'from_date': params['date'],  # format: yyyymmdd
                'To_date': params['date'],      # format: yyyymmdd
                'ddlquery': params['query_id'],
                'HODCode': params['hod_name'],
                'Str': params['query_name'],
                'Unit' : params['unit']
            }

            yield scrapy.Request(
                self.query_url.format(urlencode(query_params)),
                self.parse_dataset,
                errback=self.handle_err, meta={'filepath': filepath}
            )

    def start_requests(self):
        '''
        This method is called when the spider opens.
        It will check if arguments for specific query, HOD code were provided.
        If they were provided then it'll query specifically for that otherwise it goes to
        the expenditures' home page and collects for all the treasuries.
        '''
        if not all(self.__dict__.values()): 
            yield scrapy.Request(self.start_urls[0], self.parse)
        else:
            params = {
            'date': self.date,
            'query_id': self.query_id,
            'query_name': self.query_name,
            'hod_name': self.hod_name,
            'unit': self.unit
            }
            pdb.set_trace()
            return self.make_dataset_request(params)

    def parse(self, response):
        '''
        Collect queryable params and make dataset queries.
        Parameters to be collected are:

        query_id,
        HODCode,
        query_text
        '''
        # collect details of query 9 that gives consolidated data.
        query_elem = response.xpath('id("ddlQuery")/option')[self.query_index]

        # extract parameters for query i.e. query id and its text.
        query_id = query_elem.xpath('./@value').extract_first()
        query_name = query_elem.xpath('.//text()').extract_first()

        # remove extra whitespaces from query text.
        query_name = parsing_utils.clean_text(query_name)

        # extract parameters for hod_code i.e.its text.
        hod_elem = response.xpath('id("cmbDpt")/option')[0]

        hod_name = hod_elem.xpath('.//@value').extract_first()

        # remove extra whitespaces from query text.
        hod_name = parsing_utils.clean_text(hod_name)

        params = {
            'date': self.date,
            'query_id': query_id,
            'query_name': query_name,
            'hod_name': hod_name,
            'unit': self.unit
            }
        return self.make_dataset_request(params)

    def parse_dataset(self, response):
        '''
        Parse each dataset page to collect the data in a csv file.
        output: a csv file named with budget_expenditures_date format.
        '''
        # header row for the file.
        heads = response.xpath('//table//tr[@class="popupheadingeKosh"]//td//text()').extract()
        # all other rows
        data_rows = response.xpath('//table//tr[contains(@class, "pope")]')

        if not data_rows:
            return

        # prepare file name and its path to write the file.
        filepath = response.meta.get('filepath')

        with open(filepath, 'w') as output_file:
            writer = csv.writer(output_file, delimiter=',')

            # write the header
            writer.writerow(heads)

            # write all other rows
            for row in data_rows:
                cols = row.xpath('.//td')
                observation = []
                for col in cols:
                    # since we need consistency in the row length,
                    # we need to extract each cell and set empty string when no data found.
                    # by default scrapy omits the cell if it's empty and it can cause inconsistent row lengths.  # pylint:disable=line-too-long
                    observation.append(col.xpath('./text()').extract_first(' '))
                writer.writerow(observation)

    def handle_err(self, failure):
        '''
        Logs the request and response details when a request fails.
        '''
        if failure.check(HttpError):
            response = failure.value.response
            request = response.request
            self.logger.error('Request: {}'.format(request))
            self.logger.error('Request headers: {}'.format(request.headers))
            self.logger.error('Response headers: {}'.format(response.headers))
