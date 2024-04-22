from ftplib import FTP

host='127.0.0.1'
user='gadiel'
password='19112019'

try:
    ftp=FTP(host,user,password)
    print('Conexión establecida')

    ftp.dir()
    ftp.cwd('public_html')
except Exception as e:
    print('Conexión errada: '+str(e))