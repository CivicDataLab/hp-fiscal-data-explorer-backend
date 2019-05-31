# -*- coding: utf-8 -*-
import csv
import os
from urllib.parse import urlencode

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError

from scraper.settings import DATASET_PATH
from scraper.utils import parsing_utils


class TreasuryBaseSpider(scrapy.Spider):
    '''
    Base spider for HP treasury. It has methods for making dataset requests
    for a given treasury's given ddo with a given query in a given date range.
    '''
    allowed_domains = ['himkosh.hp.nic.in']

    def __init__(self, *args, **kwargs):
        super(TreasuryBaseSpider, self).__init__(*args, **kwargs)
        if not hasattr(self, 'start') and not hasattr(self, 'end'):
            raise CloseSpider('No date range given!')

    def make_dataset_request(self, params):
        '''
        Construct and yield a scrapy request for a dataset.
        '''
        # generate a filepath to store the dataset in.
        filename = parsing_utils.make_dataset_file_name({
            'query': self.name, 'treasury': params['treasury_name'],
            'ddo': params['ddo_code'], 'date': '{}-{}'.format(params['start'], params['end'])
        })
        filepath = os.path.join(DATASET_PATH, filename)

        # don't request the same dataset again if it's already collected previously
        # check if a file with a particular dataset name exist, if it does then
        # also check if it's empty or not, if it's empty we request it again.
        if not os.path.exists(filepath) or not os.stat(filepath).st_size:
            query_params = {
                'from_date': params['start'],  # format: yyyymmdd
                'To_date': params['end'],      # format: yyyymmdd
                'ddlquery': params['query_id'],
                'HODCode': '{}-{}'.format(params['treasury_id'], params['ddo_code']),
                'Str': params['query_name']
            }

            yield scrapy.Request(
                self.query_url.format(urlencode(query_params)), # pylint: disable=no-member
                self.parse_dataset,
                errback=self.handle_err, meta={'filepath': filepath}
            )

    def start_requests(self):
        '''
        This method is called when the spider opens.
        It will check if arguments for specific query, treasury were provided.
        If they were provided then it'll query specifically for that otherwise it goes to
        the expenditures' home page and collects for all the treasuries.
        '''
        if (
                not hasattr(self, 'query_id')
                and not hasattr(self, 'treasury_id')
                and not hasattr(self, 'query_name')
            ):
            yield scrapy.Request(self.start_urls[0], self.parse)
        else:
            for ddo_code in self.get_ddo_codes(self.treasury_id): #pylint: disable=no-member
                params = {
                    'start': self.start,  #pylint: disable=no-member
                    'end': self.end,  #pylint: disable=no-member
                    'query_id': self.query_id,  #pylint: disable=no-member
                    'treasury_id': self.treasury_id,  #pylint: disable=no-member
                    'ddo_code': ddo_code,
                    'query_name': self.query_name  #pylint: disable=no-member
                }
                yield self.make_dataset_request(params)

    def parse(self, response):
        '''
        Collect queryable params and make dataset queries.
        Parameters to be collected are:

        query_id,
        HODCode: constructed by joining treasury_code-ddo_code
        query_text
        '''
        # collect details of query 10 that gives consolidated data.
        query_elem = response.xpath('id("ddlQuery")/option')[self.query_index]  # pylint: disable=no-member

        # extract parameters for query i.e. query id and its text.
        query_id = query_elem.xpath('./@value').extract_first()
        query_name = query_elem.xpath('.//text()').extract_first()

        # remove extra whitespaces from query text.
        query_name = parsing_utils.clean_text(query_name)

        # collect all treasury names from dropdown.
        treasuries = response.xpath('id("cmbHOD")/option')

        # for each treasury for each ddo, make requests for datasets for the given date range and query.  # pylint: disable=line-too-long
        for treasury in treasuries[1:]:
            treasury_id = treasury.xpath('./@value').extract_first()
            treasury_name = treasury.xpath('.//text()').extract_first()
            treasury_name = parsing_utils.clean_text(treasury_name)

            for ddo_code in self.get_ddo_codes(treasury_id):
                params = {
                    'start': self.start,  #pylint: disable=no-member
                    'end': self.end,  #pylint: disable=no-member
                    'query_id': query_id,
                    'treasury_id': treasury_id,
                    'treasury_name': treasury_name,
                    'ddo_code': ddo_code,
                    'query_name': query_name
                }
                return self.make_dataset_request(params)

    def parse_dataset(self, response):  #pylint: disable=no-self-use
        '''
        Parse each dataset page to collect the data in a csv file.
        output: a csv file named with query_treasury-ddo_year(all lowercase) format.
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

    def get_ddo_codes(self, treasury_id):
        '''
        collects and return ddo code for a treasury.
        '''
        ddo_file_path = os.path.join(DATASET_PATH, '{}_ddo_codes.csv'.format(treasury_id))

        if os.path.exists(ddo_file_path):

            with open(ddo_file_path) as ddo_file:
                ddo_code_reader = csv.reader(ddo_file)
                next(ddo_code_reader)  # pylint: disable=stop-iteration-return

                for ddo in ddo_code_reader:
                    ddo_code = ddo[0]
                    yield ddo_code
        else:
            self.logger.error('No ddo code file exists for treasury: {}'.format(treasury_id))
