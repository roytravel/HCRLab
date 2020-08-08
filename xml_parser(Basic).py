# -*- coding:utf-8 -*-

''' SQL Table 
[Basic] = ID, Name, Abstraction, Structure, Status, Description, Extended_Description, Background_Detail, Likelihood_Of_Exploit, Functional_Area, Affected_Resource
'''


import xml.etree.ElementTree as elemTree
from xml.etree.ElementTree import parse
import xmltodict
import json


if __name__ == '__main__':

    i = 0
    result = list()
    tree = elemTree.parse('cwec_v4.1.xml')
    root = tree.getroot()
    
    # i = [Weaknesses, Categories, Views, External_References]
    for i in root:
        # j = [Weakness, Category, View, External_Reference]
        for j in i:
            if "Weakness" in j.tag:
                ID = j.attrib.get('ID')
                Name = j.attrib.get('Name').replace("'", '')
                Abstraction = j.attrib.get('Base')
                Structure = j.attrib.get('Simple')
                Status = j.attrib.get('Incomplete')

                for k in j:
                    # k = [Description, Background_Details, Likelihood_Of_Exploit, Functional_Area, Affected_Resource, ...]
                    if "Description" in k.tag:

                        if ("Extended_Description") in k.tag:
                            try:
                                Extended_Description = k.text.replace('\n            ','').replace("'","").replace('\n\t   ','').replace('    ','').replace('\n','').replace('				','')
                            except:
                                pass
                                Extended_Description = k.text
                        else:
                            Description = k.text.replace('\n\t\t\t   ','').replace('\n','').replace("'",'')
                            

                    if "Background_Details" in k.tag:
                        Background_Detail = list()
                        for l in k:
                            Background_Detail.append(l.text.replace('\n               ','').replace("'",''))

                    if "Likelihood_Of_Exploit" in k.tag:
                        Likelihood_Of_Exploit = k.text


                    if "Functional_Area" in k.tag:
                        Functional_Area = k.text.replace('\n            ','')
                        

                    if "Affected_Resource" in k.tag:
                        Affected_Resource = k.text.replace('\n            ','')

                try:
                    for z in range(len(Background_Detail)):
                        query = "INSERT INTO Vulnerability_DB.CWE_Weakness_Basic (ID, Name, Abstraction, Structure, Status, Description, Extended_Description, Background_Detail, Likelihood_Of_Exploit, Functional_Area, Affected_Resource) VALUES ('{}','{}','{}','{}','{}','{}','{}', '{}', '{}', '{}', '{}');".format(ID, Name, Abstraction, Structure, Status, Description, Extended_Description, Background_Detail[z], Likelihood_Of_Exploit, Functional_Area, Affected_Resource)
                        result.append(query)
                except Exception as e:
                    pass

    with open('Vulnerability_DB.CWE_Weakness_Basic.sql', 'a+') as f:

        for y in range(len(result)):
            f.write(result[y])
            f.write('\n')