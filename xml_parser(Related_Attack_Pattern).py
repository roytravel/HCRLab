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
                    # k = [Description, Background_Details, Likelihood_Of_Exploit, Functional_Area, Affected_Resource, Common Consequence, Related_attack_Patterns...]

                    if "Related_Attack_Patterns" in k.tag:
                        for l in k:
                            
                            if "Related_Attack_Pattern" in l.tag:
                                
                                query = "INSERT INTO Vulnerability_DB.CWE_Weakness_Related_Attack_Pattern (ID, CAPEC_ID) VALUES ('{}', '{}');".format(ID, l.attrib.get("CAPEC_ID"))
                                with open('Vulnerability_DB.CWE_Weakness_Related_Attack_Pattern.sql', 'a+') as f:
                                    f.write(query)
                                    f.write('\n')
