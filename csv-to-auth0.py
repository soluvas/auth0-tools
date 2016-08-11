import csv
import json
# import bcrypt

# read CSV and create array
users = []
with open('in/user.prd.2016-08-09.csv', 'r') as inf:
    csvreader = csv.DictReader(inf)
    for row in csvreader:
        # print(row)
        # salt = bcrypt.gensalt()
        # hash = bcrypt.hashpw(row.password, salt)
        user = {
            'email_verified': row['id_usergroup'] == 2,
            'email': row['id_user'] + '@fake.eragano.com',
            'username': row['username'],
            'app_metadata': {
                'user_num': row['id_user'],
                # 'password': hash,
                'role': row['sebagai'],
                'usergroup_id': row['id_usergroup'],
            },
            'user_metadata': {
                'name': row['nama_lengkap'],
                'birth_place': row['tempat_lahir'],
                'birth_date': row['tanggal_lahir'],
                'address_street': row['alamat'],
                'address_village': row['desa_kelurahan'],
                'address_district': row['kecamatan'],
                'address_locality': row['kabupaten_kota'],
                'address_region': row['provinsi'],
                'address_postal_code': row['kodepos'],
                'mobile_number': row['no_telepon'],
                'gov_card_number': row['no_ktp'],
                'gov_card_expiration_date': row['tanggal_ktp'],
                'schedule_id': row['id_jadwal']
            }
        }
        users.append(user)

# output JSON
with open('out/auth0-from-csv.json', 'w') as outf:
    json.dump(users, outf)
