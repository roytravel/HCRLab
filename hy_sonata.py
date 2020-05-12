# Who       : Roytravel
# When      : 2020.05.12
# Why       : To check traffic in the vehicle named YF SONATA
# How       : Use pandas framework to handling matrix data
# What      : Analysis Tool
# Where     : Hacking and Countermeasure Response Lab

import os
import pandas as pd

class DataFrame(object):
    def __init__(self):
        pass

    def get_frame(self, fullpath, column_name):
        ''' load dataframe and add a column name '''
        frame = pd.read_csv(fullpath)
        data = frame.values.tolist()
        dataFrame = pd.DataFrame(data, columns=column_name)
        return dataFrame


    def get_shape(self, dataFrame):
        '''
        check dataframe by matrix
        #>(581362, 5) static
        #>(911109, 5) drive
        '''
        return dataFrame.shape


    def get_unique_column(self, dataFrame):
        distict_message = dataFrame['MID'].unique().tolist()
        return distict_message


    def get_unique_data_by_column(self, dataFrame, messageID):
        data = dataFrame[dataFrame['MID'] == messageID]
        return data

    def get_count_by_time(self, dataFrame):
        timeList = dataFrame['Timestamp'].tolist()
        totalTime = timeList[-1] - timeList[0]
        seconds = round((len(timeList) / totalTime), 3)
        minutes = round(len(timeList) / (totalTime/60) ,3)
        return totalTime, seconds, minutes


def get_fullpath(path):
    for root, dirs, files in os.walk(path):
        fullpath = list()
        for file in files:
            fullpath.append(root + file)
    return fullpath



if __name__ == '__main__':

    column_name = ['Timestamp', 'MID', 'Length', 'Data', 'Flag']
    fullpath = get_fullpath("C:/HY_SONATA/")
    DF = DataFrame()
    

    for idx in range(len(fullpath)):
        print ("[{}]".format(fullpath[idx]))
        dataFrame = DF.get_frame(fullpath[idx], column_name)

        distinct_message = DF.get_unique_column(dataFrame)

        for index in range(len(distinct_message)):
            data = DF.get_unique_data_by_column(dataFrame, distinct_message[index])
            print ("0x{} : {}".format(distinct_message[index],len(data['Data'].unique().tolist())))

        print ("[+] MID 개수 : {}".format(len(distinct_message)))

        totalTime, seconds, minutes = DF.get_count_by_time(dataFrame)
        
        print ("전체 시간 : {}초".format(totalTime))
        print ("초당 개수 : {}개".format(seconds))
        print ("분당 개수 : {}개".format(minutes))
        print (DF.get_shape(dataFrame))
        print ('\n')

