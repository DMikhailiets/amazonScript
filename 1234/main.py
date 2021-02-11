import os
import csv
import subprocess
from awscli.customizations.ec2 import runinstances


ami_id = 'ami-0885b1f6bd170450c'  # ubuntu
true = True
false = False


def get_out(cmd: str):
    output = subprocess.check_output(cmd, shell=True)
    output = eval(output.decode('utf-8'))
    return output


with open('credentials.csv', 'r') as csvfile:
    fields = ['User name', 'Password', 'Access key ID', 'Secret access key',  'Console login link']
    reader = csv.DictReader(csvfile, fieldnames=fields)
    for row in reader:
        keyid = row['Access key ID']
        access_key = row['Secret access key']

os.system(f'aws configure set aws_access_key_id {keyid}')
os.system(f'aws configure set aws_secret_access_key {access_key}')
# os.system(f'aws ec2 create-image --instance-id=1 --name="test"')
key_pairs = get_out('aws ec2 describe-key-pairs')


if not key_pairs['KeyPairs']:
    os.system('aws ec2 create-key-pair --key-name chirp-root --output text > chirp-root-key-pair.pem')

sec_groups = get_out('aws ec2 describe-security-groups')


if len(sec_groups['SecurityGroups']) == 1:
    print(len(sec_groups))

    vpc_id = get_out('aws ec2 describe-vpcs')

    vpc_id = vpc_id['Vpcs'][0]['VpcId']
    print(f'VPC_ID: {vpc_id}')
    group = get_out(f'aws ec2 create-security-group --group-name chirp-sg --description "blanc" --vpc-id {vpc_id}')

# sec_groups = get_out('aws ec2 describe-security-groups')
# sec_groups_id = sec_groups['SecurityGroups'][0]['GroupId']
# perm = os.system(f'aws ec2 authorize-security-group-ingress --group-id {sec_groups} --protocol tcp --port 22')


sec_groups = get_out('aws ec2 describe-security-groups')
sec_groups_id = sec_groups['SecurityGroups'][0]['GroupId']

key_name = get_out('aws ec2 describe-key-pairs')['KeyPairs'][0]['KeyName']

os.system(f'aws ec2 run-instances --image-id {ami_id} --count 1 --instance-type t2.micro --key-name {key_name} --security-group-ids {sec_groups_id}')
