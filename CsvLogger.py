
import logging
import time
from csv import writer

from StationStatus import StationStatus


class CsvLogger:
    file = ''
    previousStatus=None

    def __init__(self, fileName='/home/funghi/raspstation/stats.csv'):
        self.file=fileName

    def logStatus(self, s: StationStatus):
        try:
            if (not s.equals(self.previousStatus)):
                self.previousStatus=s.clone()
                # contents with humidifier info
                row_contents = [time.strftime('%d/%m/%y %H:%M:%S'),'{:0.1f}'.format(s.temperature),'{:0.1f}'.format(s.humidity),s.isFanEnabled,s.isHeatEnabled, s.isHumidifierEnabled]

                # contents without humidifier info
                #row_contents = [time.strftime('%d/%m/%y %H:%M:%S'),'{:0.1f}'.format(s.temperature),'{:0.1f}'.format(s.humidity),s.isFanEnabled,s.isHeatEnabled]
                self.__appendListAsRow(row_contents)
        except Exception as e:
            print("An error ocurred storing csv register: ", e)


    def __appendListAsRow(self, list_of_elem):
        # Open file in append mode
        with open(self.file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)