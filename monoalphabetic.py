# -*- coding:utf-8 -*-
import operator


def descending(dictionary : dict):
    '''Data in descending order'''
    return dict(sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True))


def statistic(ciphertext : str):
    '''Get statistic from ciphertext'''
    statistic_dict = dict()

    for idx in ciphertext:
        if idx in statistic_dict:
            statistic_dict[idx] = statistic_dict[idx] + 1
        else:
            statistic_dict[idx] = 1

    return statistic_dict


def print_value(dictionary):
    for key, value in dictionary.items():
        if len(key)==3:
            print('[{}] : {} ({}%)'.format(key, value, round(value / (len(ciphertext)/3),3)))
        else:
            print('[{}] : {} ({}%)'.format(key, value, round(value / len(ciphertext),3)))


def get_word_statistic(ciphertext : str):
    word = [ciphertext[x:x+2] for x in range(len(ciphertext))]
    word_dict = dict()

    for idx in word:
        try:
            word_dict[idx] += 1
        except:
            word_dict[idx] = 1
    
    word_dict = descending(word_dict)
    return word_dict


def diffing(ciphertext):
    '''Get mapping table'''
    plaintext = "whensatoshinakamotofirstsetthebitcoinblockchainintomotioninjanuaryhewassimultaneouslyintroducingtworadicalanduntestedconceptsthefirstisthebitcoinadecentralizedpeertopeeronlinecurrencythatmaintainsavaluewithoutanybackingintrinsicvalueorcentralissuersofarthebitcoinasacurrencyunithastakenupthebulkofthepublicattentionbothintermsofthepoliticalaspectsofacurrencywithoutacentralbankanditsextremeupwardanddownwardvolatilityinpricehoweverthereisalsoanotherequallyimportantparttosatoshisgrandexperimenttheconceptofaproofofworkbasedblockchaintoallowforpublicagreementontheorderoftransactionsbitcoinasanapplicationcanbedescribedasafirsttofilesystemifoneentityhasbtcandsimultaneouslysendsthesamebtctoaandtobonlythetransactionthatgetsconfirmedfirstwillprocessthereisnointrinsicwayofdeterminingfromtwotransactionswhichcameearlierandfordecadesthisstymiedthedevelopmentofdecentralizeddigitalcurrencysatoshisblockchainwasthefirstcredibledecentralizedsolutionandnowattentionisrapidlystartingtoshifttowardthissecondpartofbitcoinstechnologyandhowtheblockchainconceptcanbeusedformorethanjustmoney"

    map_dict = dict()

    for idx in range(len(ciphertext)):
        map_dict[ciphertext[idx]] = plaintext[idx]

    for key, value in map_dict.items():
        print ('[평문 : {}] : 암호 : {}'.format(value,key))
    

if __name__ == '__main__':

    # 암호문 정의
    ciphertext = "jpngvcbyvpzgcscqybyozivbvnbbpnrzbmyzgrfymsmpczgzgbyqybzygzgecgacikpnjcvvzqafbcgnyavfkzgbiyxamzgdbjyicxzmcfcgxagbnvbnxmygmnhbvbpnozivbzvbpnrzbmyzgcxnmngbicfzlnxhnnibyhnniygfzgnmaiingmkbpcbqczgbczgvcucfanjzbpyabcgkrcmszgdzgbizgvzmucfanyimngbicfzvvanivyocibpnrzbmyzgcvcmaiingmkagzbpcvbcsngahbpnrafsyobpnharfzmcbbngbzygrybpzgbniqvyobpnhyfzbzmcfcvhnmbvyocmaiingmkjzbpyabcmngbicfrcgscgxzbvntbinqnahjcixcgxxyjgjcixuyfcbzfzbkzghizmnpyjnunibpninzvcfvycgybpninwacffkzqhyibcgbhcibbyvcbyvpzvdicgxnthnizqngbbpnmygmnhbyochiyyoyojyisrcvnxrfymsmpczgbycffyjoyiharfzmcdinnqngbygbpnyixniyobicgvcmbzygvrzbmyzgcvcgchhfzmcbzygmcgrnxnvmizrnxcvcozivbbyozfnvkvbnqzoygnngbzbkpcvrbmcgxvzqafbcgnyavfkvngxvbpnvcqnrbmbyccgxbyrygfkbpnbicgvcmbzygbpcbdnbvmygoziqnxozivbjzffhiymnvvbpninzvgyzgbizgvzmjckyoxnbniqzgzgdoiyqbjybicgvcmbzygvjpzmpmcqnncifznicgxoyixnmcxnvbpzvvbkqznxbpnxnunfyhqngbyoxnmngbicfzlnxxzdzbcfmaiingmkvcbyvpzvrfymsmpczgjcvbpnozivbminxzrfnxnmngbicfzlnxvyfabzygcgxgyjcbbngbzygzvichzxfkvbcibzgdbyvpzobbyjcixbpzvvnmygxhcibyorzbmyzgvbnmpgyfydkcgxpyjbpnrfymsmpczgmygmnhbmcgrnavnxoyiqyinbpcgeavbqygnk"

    # 알파벳 통계 
    statistic_dict = statistic(ciphertext)

    # 통계 내림차순 정렬
    data = descending(statistic_dict)

    # 자주 사용되는 세자리 알파벳 추출
    word_dict = get_word_statistic(ciphertext)

    # 알파벳 통계 내림차순 출력
    print_value(data)

    # 자주 사용되는 세자리 알파벳 통계 내림차순 출력
    print_value(word_dict)
