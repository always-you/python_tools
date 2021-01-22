import json
import requests
from random import randint
from hashlib import md5


def youdao_translator(content):
    """
    有道翻译，访问太频繁会被封ip
    """
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = dict()
    # 调接口时所需参数，看自己情况修改，不改也可调用
    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = ''
    data['sign'] = ''
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    res = requests.get(url, params=data)
    data = json.loads(res.content.decode('utf-8'))
    # 取出需要的数据
    result = data['translateResult']
    ret = ''
    for i in range(len(result)):
        line = ''
        for j in range(len(result[i])):
            line = result[i][j]['tgt']
        ret += line + '\n'
    return ret


def baidu_translate(content, appid, key, _from='auto', to='zh'):
    """
    百度翻译普通版，频率限制1s/次，不限量
    """
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = randint(10000000, 99999999)
    appid = appid
    key = key

    data = {
        'q': content,
        'from': _from,
        'to': to,
        'appid': appid,
        'salt': salt,
        'sign': md5((appid+content+str(salt)+key).encode('UTF-8')).hexdigest()
    }
    res = requests.get(url, params=data)
    res = json.loads(res.text)
    return res['trans_result'][0]['dst']


if __name__ == '__main__':
    print(youdao_translator('content'))

