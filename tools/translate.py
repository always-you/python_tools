import urllib.request
import urllib.parse
import json


def youdao_translate(content):
    '''有道翻译'''
    youdao_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {}
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
    data = urllib.parse.urlencode(data).encode('utf-8')
    # 发送翻译请求
    youdao_response = urllib.request.urlopen(youdao_url, data)
    # 获得响应
    youdao_html = youdao_response.read().decode('utf-8')
    target = json.loads(youdao_html)
    # 取出需要的数据
    trans = target['translateResult']
    ret = ''
    for i in range(len(trans)):
        line = ''
        for j in range(len(trans[i])):
            line = trans[i][j]['tgt']
        ret += line + '\n'
    return ret

if __name__ == '__main__':
    print(youdao_translate('cactus'))

