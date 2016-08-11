# Auth0 WILL send SMS verification code using Twilio!
# Workaround: in Twilio, during import, disable sending to target region

import csv
import json
import urllib.request
# import bcrypt
import re
import uuid
import yaml

def fix_localdate(indodate):
    m = re.search('^(\d{2})-(\d{2})-(\d{2})$', row['no_telepon'])
    if m:
        m.group(3) + '-' + m.group(2) + '-' + m.group(1)
    else:
        None

# TODO
with open('config.yaml', 'r') as yamlf:
    config = yaml.load(yamlf)

# read CSV and create array
users = []
with open('in/user.prd.2016-08-09.csv', 'r') as inf:
    csvreader = csv.DictReader(inf)
    for row in csvreader:
        # print(row)
        # salt = bcrypt.gensalt()
        # hash = bcrypt.hashpw(row['password'].encode('utf8'), salt).decode('utf8')
        user = {
            #'email_verified': row['id_usergroup'] == 2,
            #'email': row['id_user'] + '@fake.eragano.com',
            #'username': row['username'],
            #'password': row['password'],
            'name': row['nama_lengkap'],
            'nickname': row['username'],
            'app_metadata': {
                # 'username': row['username'],
                'user_num': row['id_user'],
                # 'password': hash,
                'role': row['sebagai'],
                'usergroup_id': row['id_usergroup'],
                'schedule_id': row['id_jadwal']
            },
            'user_metadata': {
                'birth_place': row['tempat_lahir'],
                'birth_date': fix_localdate(row['tanggal_lahir']),
                'address_street': row['alamat'],
                'address_village': row['desa_kelurahan'],
                'address_district': row['kecamatan'],
                'address_locality': row['kabupaten_kota'],
                'address_region': row['provinsi'],
                'address_postal_code': row['kodepos'],
                # 'mobile_number': row['no_telepon'],
                'gov_card_number': row['no_ktp'],
                'gov_card_expiration_date': fix_localdate(row['tanggal_ktp'])
            }
        }

        # if not row['password']: # password is mandatory
        #     user['password'] = str(uuid.uuid4())

        # Mobile number
        if re.search('^08\d+$', row['no_telepon']):
            mobile_number = re.compile('^08').sub('+628', row['no_telepon'])
            user['phone_number'] = mobile_number
            user['phone_verified'] = True # FIXME: not accepted!
            #user['app_metadata']['phone_number'] = mobile_number
        else:
            # will be rejected anyway
            user['app_metadata']['phone_number'] = row['no_telepon']

        user['connection'] = 'sms'
        print(user)
        req = urllib.request.Request('https://eragano.auth0.com/api/v2/users',
            data=json.dumps(user).encode('utf8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + config['auth0-token']
            })
        try:
            resp = urllib.request.urlopen(req)
            print(resp.read())
        except urllib.error.HTTPError as e:
            print(e.read())
            #exit(1) # ignore and go
        users.append(user)

# output JSON
# with open('out/auth0-from-csv.json', 'w') as outf:
#     json.dump(users, outf)
