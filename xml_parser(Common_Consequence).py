# -*- coding:utf-8 -*-

''' SQL Table 
Common_Consequence = ID, Scope, Scope_count, Impact, Impact_count, Likelihood, Note
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
                for k in j:
                    # k = [Description, Background_Details, Likelihood_Of_Exploit, Functional_Area, Affected_Resource, Common Consequence, ...]

                    if "Common_Consequences" in k.tag:
                        # l은 Common_Consequence 개수 
                        for l in k:
                            
                            if "Consequence" in l.tag:
                                # l의 개수는 한 Common_Consequence에 있는 

                                Scope = list()
                                Impact = list()

                                # 요소 iteration
                                for m in l:
                                    category = m.tag.replace('{http://cwe.mitre.org/cwe-6}','')

                                    if (category == "Scope"):
                                        Scope.append(m.text)

                                    if (category == "Impact"):
                                        Impact.append(m.text)

                                    if (category == "Note"):
                                        try:
                                            Note = m.text.replace('\n','').replace('"',"'")
                                        except:
                                            Note = m.text
                                            


                            query = 'INSERT INTO Vulnerability_DB.CWE_Weakness_Common_Consequence (ID, Scope, Scope_count, Impact, Impact_count, Note) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(ID, Scope, len(Scope), Impact, len(Impact), Note)

                            with open('Vulnerability_DB.CWE_Weakness_Common_Consequence.sql', 'a+') as f:
                                f.write(query)
                                f.write('\n')
