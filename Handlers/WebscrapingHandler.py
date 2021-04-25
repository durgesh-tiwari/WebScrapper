from Components.LoggerComponent import debug
from Components.BaseComponent import BaseComponent
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import os


class WebscrapingHandler(BaseComponent):

    @debug
    def __init__(self):
        super(WebscrapingHandler, self).__init__()
        self.url = ''
        self.html_content = ''
        self.date_col_value = []
        self.prev_date = ''
        self.next_date = ''
        self.df_cols = ['Date', 'Dollars per Million Btu']
        self.OUTPUT_DIR = os.path.join(self.BASE_DIR, "Output")
        if not os.path.exists(self.OUTPUT_DIR):
            os.mkdir(self.OUTPUT_DIR)

    @debug
    def read_input_data(self):
        try:
            url = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'
            self.html_content = requests.get(url).text
            self.soup = BeautifulSoup(self.html_content, "lxml")
            self.henry_table = self.soup.find("table", summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
        except Exception as e:
            self.handle_exception(e)

    @debug
    def process_input_data(self):
        try :
            counter = 0
            c = 1
            for td in self.henry_table.find_all('td'):
                if counter % 6 == 0:
                    if td.text.replace('\n', ' ').strip() == '':
                        continue
                    else:
                        date_list = [i.strip() for i in td.text.replace('\n',' ').strip().split('to')]
                        self.prev_date = pd.to_datetime(date_list[0].replace('-',''))
                        c = 1
                else:
                    if c == 1:
                        self.date_col_value.append([self.prev_date,td.text.replace('\n',' ').strip()])
                        c = 0
                    else:
                        self.next_date = self.prev_date + datetime.timedelta(days=1)
                        self.prev_date = self.next_date
                        self.date_col_value.append([self.next_date,td.text.replace('\n',' ').strip()])
                counter = counter + 1
        except Exception as e:
            self.handle_exception(e)

    @debug
    def write_output_data(self):
        try:
            self.date_per_btu_df =  pd.DataFrame(self.date_col_value)
            self.date_per_btu_df.columns = self.df_cols
            self.date_per_btu_df.to_csv(os.path.join(self.OUTPUT_DIR,'Henry Hub Natural Gas Spot Price (Dollars per Million Btu).csv'), index=False)
        except Exception as e:
            self.handle_exception(e)

