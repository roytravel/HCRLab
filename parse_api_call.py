import os
from collections import Counter
import xlsxwriter as xlsx
import re

class LogParser(object):

    def __init__(self):
        pass

    ## 파일의 전체 경로 리스트를 생성 및 반환
    def get_log_file(self):
        for root, dirs, files in os.walk("C:/logFile"):
            fullpath = list()
            root = root + '/'
            for file in files:
                path = root + file
                fullpath.append(path)
        
        return fullpath


    ## 읽고, API 카운트 하는 모듈
    def count_api(self,fullpath):
        with open(fullpath, mode = 'rt', encoding='utf-8', errors='ignore') as file:
            # print (fullpath)
            data = file.readlines()

            dic = Counter()
            dic2 = dict()
            errorCount = 0

            for index in range(len(data)):
                try:
                    if (('~~ ' in data[index]) and ('arg ' not in data[index]) and ('type=' not in data[index]) and ('0x' not in data[index])):
                        temp = data[index].split('!')
                        #ex) temp[0] = ntdll.dll, 
                        #ex) temp[1] = 'RtlEncodePointer'
                        temp[0] = temp[0].split('~~ ')[1]
                        temp[1] = temp[1].strip("\n")

                        # if '~~' in temp[1]:
                        #     temp[1] = temp[1].split('~~')[0]

                        p = re.compile("~~[0-9]{3,5}~~")
                        result = p.findall(temp[1])
                        if (len(result) >=1):
                            continue

                        if '.dll' in temp[1]:
                            continue
                        
                        dic[temp[1]] += 1
                        dic2[temp[1]] = temp[0]

                except Exception as e:
                    errorCount += 1
                    continue

        return dic, dic2


    ##개별 파일에 대한 API 카운트를 계산
    def save_api(self, fullpath, dic3):
        for k,v in dic3.items():
            for x,y in v.items():
                # print ("{} : {} : {}".format(x,k,y))
                with open(fullpath+".txt", mode = 'a+', encoding='utf-8', errors = 'ignore') as g:
                    g.write("\n{}-{}-{}".format(x,k,y))
                    g.write("\n")
        print ("[+] Save API count by each file: {}".format(fullpath))


    ## API 합계 모듈
    def get_dic_count(self, dicList):
        print ("[+] Start Count API by Name")
        dict2 = Counter()
        dict3 = dict()
        for j in range(len(dicList)):
            # k = API, x = DLL, y = CNT
            for k, v in sorted(list(dicList[j].items())):
                for x, y in v.items():

                    dict2[k] += y

                    dict3[k] = x

            print("  [-] API Count : {}".format(len(dicList[j])))

        return dict2, dict3


    def make_sum_by_descend(self, dict2, dict3):
                
        dict4 = dict()

        dict2 = dict(sorted(list(dict2.items()), key = lambda x: x[1], reverse=True))

        for k,v in dict2.items():

            dict4[k] = {dict3[k]:v}

        return dict4


    def get_total_count_api(self, dict4):
        for k,v in dict4.items():
            for x, y in v.items():
                with open("C:/logFile/result.txt", mode = 'a+', encoding='utf-8', errors = 'ignore') as g:
                    g.write("\n{}.{}.{}".format(x,k,y))
                    g.write("\n")


    def api_count_with_dll(self, dic, dic2):
        dic3 = dict()
        dic = dict(dic)
        dic = dict(sorted(list(dic.items()), key = lambda x: x[1], reverse=True))
        
        for key, value in dic.items():
            dic3[key] = {dic2[key]:dic[key]} #API : {DLL : CNT}
        return dic3


if __name__ == '__main__':

    LP = LogParser()


    # 파일의 전체 경로 리스트를 생성 및 반환
    fullpath = LP.get_log_file()

    dicList = list()

    #각각의 로그 파일에 대한 DLL, API, CNT 정보를 텍스트 파일로 추출
    for index in range(len(fullpath)):
        # 읽고, API 카운트 하는 모듈
        dic, dic2 =  LP.count_api(fullpath[index])
        
        dic3 = LP.api_count_with_dll(dic, dic2)
        
        #개별 파일에 대한 API 카운트를 로깅
        LP.save_api(fullpath[index], dic3)

        dicList.append(dic3)
    
        

    dict2, dict3 = LP.get_dic_count(dicList)

    dict4 = LP.make_sum_by_descend(dict2, dict3)

    LP.get_total_count_api(dict4)



    wb=xlsx.Workbook("C:/logFile/result.xlsx")
    ws=wb.add_worksheet()

    # 엑셀 셀 속성 설정
    format0=wb.add_format({'border':2,'bold':True,'align':'center','fg_color':'white','font_color':'black'})
    format1=wb.add_format({'border':1,'bold':True,'align':'center','fg_color':'white','font_color':'black'})

    # 엑셀 셀 너비 설정
    ws.set_column('A:A',20)
    ws.set_column('B:B',20)
    ws.set_column('C:C',20)
    ws.set_column('D:D',10)

    # (x+1,y+1)의 위치에 데이터 입력 및 셀 속성 설정
    ws.write(0,0,u'DLL',format0)
    ws.write(0,1,u'API',format0)
    ws.write(0,2,u'SUM',format0)

    # 파일 이름을 컬럼 명으로 지정
    for idx in range(len(fullpath)):
        ws.set_column(idx+4,idx+5,30)
        ws.write(0,idx+4,fullpath[idx].split('/')[-1])


    # TOTAL RESULT(DLL & API & SUM)를 기입
    for i, kv in enumerate(dict4.items()):
        for j in kv[1]:
            ws.write(i+1,0,list(kv[1])[0])
            ws.write(i+1,1,kv[0])
            ws.write(i+1,2,kv[1][j])


    for jdx in range(len(fullpath)):
        record = list()
        with open(fullpath[jdx]+".txt", mode = 'rt', encoding='utf-8', errors='ignore') as file:
            read = file.readlines()

            #하나의 파일에서 DLL, API, CNT를 리스트화
            for line in range(len(read)):
                if '-' in read[line]:
                    a,b = divmod(line,2)
                    ws.write(a+b,jdx+4,read[line])
            print ("[+] Finished : {}".format(fullpath[jdx]))

    wb.close()
