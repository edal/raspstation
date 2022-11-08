
import time
from csv import writer

from StationStatus import StationStatus


class CsvLogger:
    file = ''

    def __init__(self, fileName='/home/funghi/raspstation/stats.csv'):
        self.file=fileName

    def logStatus(self, s: StationStatus):
        row_contents = [time.strftime('%d/%m/%y %H:%M:%S'),'{:0.1f}'.format(s.temperature),'{:0.1f}'.format(s.humidity),s.isFanEnabled,s.isHeatEnabled, s.isHumidifierEnabled]
        self.__appendListAsRow(row_contents)


    def __appendListAsRow(self, list_of_elem):
        # Open file in append mode
        with open(self.file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)