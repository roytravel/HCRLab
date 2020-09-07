# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:51:27 2020

@author: roytravel
"""
import pandas as pd
from glob import glob

   
class Class(object):
    
    def __init__(self):
        self.test = sorted([x for x in glob("./_0903_Data/*test.txt")])
        self.train = sorted([x for x in glob("./_0903_Data/*training*.txt")])
    

    def _dataframe_from_csv(self, target):
        return pd.read_csv(target)
    
    
    def _dataframe_from_csvs(self, targets):
        return pd.concat([_dataframe_from_csv(x) for x in targets])


    def class_remover(self):
        for idx in self.test:
            df = pd.read_csv(idx)
            class_dropped_df = df.drop(['Class'], axis='columns', inplace=False)
            class_dropped_df.to_csv(idx, index=False)
        print('[+] Test dataset에 대한 Class 제거 작업이 완료되었습니다.')
        
        
    def class_spliter(self):
        for idx in self.train:
            df = pd.read_csv(idx)
            
            # 데이터프레임에 열 추가
            df['SubClass'] = df['Class']
            
            # SubClass의 Normal 값 제거
            df['SubClass'] = df['SubClass'].replace('Normal','Normal')
    
            #  Class의 라벨 이진화
            df['Class'] = df['Class'].replace('Flooding','Attack')
            df['Class'] = df['Class'].replace('Spoofing','Attack')
            df['Class'] = df['Class'].replace('Replay','Attack')
            df['Class'] = df['Class'].replace('Fuzzing','Attack')
            df.to_csv(idx, index=False)
        print('[+] Training dataset에 대한 Class 정제 작업이 완료되었습니다.')
    
    def statistic(self):
        for idx in self.train:
            df = pd.read_csv(idx)
            value_count = df['SubClass'].value_counts()
            print (idx)
            print (value_count)
            print ('\n')
        print("[+] Training dataset에 대한 통계치 추출이 완료되었습니다.")
    


if __name__ == '__main__':

    C = Class()
    C.class_remover()
    C.class_spliter()
    C.statistic()
    
    
    