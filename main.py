import os
import csv
import subprocess
from awscli.customizations.ec2 import runinstances
# runinstances.


with open('credentials.csv', 'r') as csvfile:
    fields = ['User name', 'Password', 'Access key ID', 'Secret access key',  'Console login link']
    reader = csv.DictReader(csvfile, fieldnames=fields)
    for row in reader:
        keyid = row['Access key ID']
        access_key = row['Secret access key']

os.system(f'aws configure set aws_access_key_id {keyid}')
os.system(f'aws configure set aws_secret_access_key {access_key}')
# os.system(f'aws ec2 create-image --instance-id=1 --name="test"')
output = subprocess.check_output('aws ec2 describe-key-pairs', shell=True)


if not eval(output.decode('utf-8'))['KeyPairs']:
    os.system('aws ec2 create-key-pair --key-name chirp-root --output text > first chirp-root-key-pair.pem')




# os.system('test')
