# -*- encoding: utf-8 -*-
import json
import os

#----------------------------------------------------------------------------
# ID, Description, CVSSv2_Vector, CVSSv2_Score, CVSSv2_Exploitability_Score, 
# CVSSv2_Impact_Score, Obtain_All_Privilege, Obtain_User_Privilege, 
# Obtain_Other_Privilege, User_Interaction_Required, CVSSv3_Vector, 
# CVSSv3_Score, CVSSv3_Exploitability_Score, CVSSv3_Impact_Score, 
# CVE_Data_Timestamp, Published_Date, Last_Modified_Date
#----------------------------------------------------------------------------


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


# 로딩된 JSON 파일을 받아서 파싱 & 파싱 데이터를 SQL 포맷화
def parse_json(data_json, idx):
    try:
        ID = data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID']
        Description = data_json['CVE_Items'][idx]['cve']['description']['description_data'][0]['value'].replace("\'","\\'")
        CVE_Data_Timestamp = data_json['CVE_data_timestamp']
        Published_Date = data_json['CVE_Items'][idx]['publishedDate']
        Last_Modified_Date = data_json['CVE_Items'][idx]['lastModifiedDate']
        # print (ID, CVE_Data_Timestamp, Published_Date, Last_Modified_Date)

        #baseMetricV3
        CVSSv3_Vector = data_json['CVE_Items'][idx]['impact']['baseMetricV3']['cvssV3']['vectorString']
        CVSSv3_Score = data_json['CVE_Items'][idx]['impact']['baseMetricV3']['cvssV3']['baseScore']
        CVSSv3_Exploitability_Score = data_json['CVE_Items'][idx]['impact']['baseMetricV3']['exploitabilityScore']
        CVSSv3_Impact_Score = data_json['CVE_Items'][idx]['impact']['baseMetricV3']['impactScore']
        # print (CVSSv3_Vector, CVSSv3_Score, CVSSv3_Exploitability_Score, CVSSv3_Impact_Score)

        #baseMtricV2
        CVSSv2_Vector = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['cvssV2']['vectorString']
        CVSSv2_Score = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['cvssV2']['baseScore']
        CVSSv2_Exploitability_Score = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['exploitabilityScore']
        CVSSv2_Impact_Score = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['impactScore']
        # print (CVSSv2_Vector, CVSSv2_Score, CVSSv2_Exploitability_Score, CVSSv2_Impact_Score)

        Obtain_All_Privilege = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['obtainAllPrivilege']
        Obtain_User_Privilege = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['obtainUserPrivilege']
        Obtain_Other_Privilege = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['obtainOtherPrivilege']
        User_Interaction_Required = data_json['CVE_Items'][idx]['impact']['baseMetricV2']['userInteractionRequired']
        # print (Obtain_All_Privilege, Obtain_User_Privilege, Obtain_Other_Privilege, User_Interaction_Required)

        query = "INSERT INTO Vulnerability_DB.CVE_Basic (ID, Description, CVSSv2_Vector, CVSSv2_Score, CVSSv2_Exploitability_Score, CVSSv2_Impact_Score, Obtain_All_Privilege, Obtain_User_Privilege, Obtain_Other_Privilege, User_Interaction_Required, CVSSv3_Vector, CVSSv3_Score, CVSSv3_Exploitability_Score, CVSSv3_Impact_Score, CVE_Data_Timestamp, Published_Date, Last_Modified_Date) VALUES ('{}', '{}', '({})', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"\
            .format(ID, Description, CVSSv2_Vector, CVSSv2_Score, CVSSv2_Exploitability_Score, CVSSv2_Impact_Score, Obtain_All_Privilege, Obtain_User_Privilege, Obtain_Other_Privilege, User_Interaction_Required,CVSSv3_Vector, CVSSv3_Score, CVSSv3_Exploitability_Score, CVSSv3_Impact_Score,CVE_Data_Timestamp, Published_Date, Last_Modified_Date)
        bquery = bytes(query, 'utf-8')
    
        return bquery
    except Exception as err:
        return False


if __name__ == '__main__':
    USER_PATH = os.environ.get('USER_PATH')
    path_json = USER_PATH + "/nvdcve-1.1-2020.json"
    path_sql = USER_PATH + '/Vulnerability_DB_CVE_Basic.sql'

    data_json = read_json(path_json)
    data_sql = read_sql(path_sql)
    deprecated_list = list()

    for idx in range(len(data_json['CVE_Items'])):
        bquery = parse_json(data_json, idx)
        #바이너리 매칭 기능 시작
        if bquery is not False:

            # 만약 CVE가 바이너리에 매칭될 경우 CVE 번호만 출력
            if (bquery[:394] in data_sql):
                print (data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'] + ' is already exist')
            
            # CVE 번호가 존재하지 않는다면 SQL 파일의 끝 부분에 업데이트
            else:
                update_sql(path_sql, bquery.decode('utf-8'))
                print (data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'] + ' is updated')
        
        # 만약 CVE가 파싱에러가 난다면 deprecated 메세지를 출력
        else:
            deprecated_list.append(data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'])
            print (data_json['CVE_Items'][idx]['cve']['CVE_data_meta']['ID'] + ' is deprecated')
    
    
    print (deprecated_list)
    print ("Deprecated CVE Count : {}".format(len(deprecated_list)))

    with open(USER_PATH + '/deprecated_cve.txt', 'a+') as d:
        for j in range(len(deprecated_list)):
            d.write(deprecated_list[j])
            d.write('\n')

    