# -*- encoding: utf-8 -*-
import json
import os


# JSON 파일 리스트 get
def get_filelist(path_json):
    fullpath = list()
    for root, dir, files in os.walk(path_json):
        root = root + '/'
        for file in files:
            path = root + file
            fullpath.append(path)

    return fullpath


# 파싱을 위해 JSON 파일 로딩
def read_json(path_json):
    with open(path_json, 'rb') as f:
        cve_data = f.read()
        data_json = json.loads(cve_data)

    return data_json


# 기존 SQL 데이터에 CVE의 존재 여부 확인을 위해 SQL 데이터 로딩
def read_sql(path_sql):
    with open(path_sql, mode='rb') as f:
        data_sql = f.read()

    return data_sql


# 기존 SQL 파일 데이터에 Add를 위한 데이터 로딩
def update_sql(path_sql, bquery):
    with open(path_sql, 'a+', -1, 'utf-8') as f:
        try:
            f.write(bquery)
            f.write('\n')
        except Exception as err:
            print (err)

    return update_sql


# 로딩된 JSON 파일을 받아서 파싱 & 파싱 데이터를 SQL 포맷화
def parse_json(data_json, idx):
    try:
        ID = data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID']
        CWE = data_json['CVE_Items'][idx]['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
        query = "INSERT INTO Vulnerability_DB.CVE_mapping_CWE (ID, CWE_ID) VALUES ('{}', '{}');".format(ID, CWE)
        bquery = bytes(query, 'utf-8')
        return bquery

    except Exception as err:
        return False


if __name__ == '__main__':
    USER_PATH = os.environ.get('USER_PATH')
    fullpath = get_filelist(USER_PATH + "/Desktop/JSON")
    path_sql = USER_PATH + '/Desktop/Vulnerability_DB_CVE_mapping_CWE_2.sql'
    data_sql = read_sql(path_sql)
    deprecated_list = list()
    # count = 0

    for i in range(len(fullpath)):
        print ("[+] {}".format(fullpath[i]))
        data_json = read_json(fullpath[i])
    
        for idx in range(len(data_json['CVE_Items'])):
            bquery = parse_json(data_json, idx)
            #바이너리 매칭 기능 시작
            if bquery is not False:

                # 만약 CVE가 바이너리에 매칭될 경우 CVE 번호만 출력
                if (bquery in data_sql):
                    print (data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'] + ' is already exist')

                    # # CVE 번호까지는 매칭되었으나, 뒤에 값이 변경된 경우를 고려해서 Fully Same일 경우.
                    # if (bquery in data_sql):
                    #     print ("Fully Same : {}".format(bquery))
                    
                    # # Partial Same으로, 데이터가 변경된 경우
                    # else:
                    #     count += 1
                    #     print ("불완벽 : {}".format(bquery))
                
                # CVE 번호가 존재하지 않는다면 SQL 파일의 끝 부분에 업데이트
                else:
                    update_sql(path_sql, bquery.decode('utf-8'))
                    print (data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'] + ' is updated')
            
            # 만약 CVE가 파싱에러가 난다면 deprecated 메세지를 출력
            else:
                deprecated_list.append(data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'])
                print (data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'] + ' is deprecated')
    
    
    # print (deprecated_list)
    print ("Deprecated CVE Count : {}".format(len(deprecated_list)))
    # print ("Duplicated : {}".format(count))

    with open(USER_PATH + '/Desktop/deprecated_cve.txt', 'a+') as d:
        for j in range(len(deprecated_list)):
            d.write(deprecated_list[j])
            d.write('\n')

    