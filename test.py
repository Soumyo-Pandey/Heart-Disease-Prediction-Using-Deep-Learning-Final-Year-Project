
import pymysql
from Crypto.Cipher import AES


key = b'@.\x8d\xfcra\xa0\x16\xd9\t\xce\x97H\x04\xb6\xee\x83r\x87\x03b\x96V\xaf<E\x83\xe8K\x12\xda\xfe'
header = b'Non sensitive information'

cipher = AES.new(key, AES.MODE_SIV)
cipher.update(header)
ciphertext, tag = cipher.encrypt_and_digest('kaleem,kaleem,1234,kaleem.mmd@gmail.com,hyd'.encode('ascii'))

data = str(ciphertext)
data1 = str(tag)


'''
db_connection = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'heartdisease',charset='utf8')
db_cursor = db_connection.cursor()
student_sql_query = "INSERT INTO users(username,password) VALUES('"+data+"','"+data1+"')"
db_cursor.execute(student_sql_query)
db_connection.commit()
'''
data = data.encode()
data1 = data1.encode()

cipher = AES.new(key, AES.MODE_SIV)
cipher.update(header)
msg = cipher.decrypt_and_verify(data, data1)
print(msg)
