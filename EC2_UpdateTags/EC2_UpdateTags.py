import json
from botocore.vendored import requests
import boto3
import urllib.parse
import csv
import os


def lambda_handler(event, context):
    # This procedure takes an input csv file and will loop through and update each ec2 instance with defined tasks in the EC2 Instance Tag Catalog
    # The csv file is an export of the current ec2 instances and correct tag information
    # this line exists mainly for the unit testing. Otherwise it is the value of the environment variable
    file = os.environ.get('CSV_FILE') if event != 'test' else context;
    updateEC2_Tags(csv_f=file)
    return {'statusCode': 200, 'body': json.dumps('lambda ec2_updatetags completed successfully')}

def ec2exist(instanceid, response):
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['InstanceId'] == instanceid:
                return True

    return False

def updateEC2_Tags(csv_f):
    sdc_session = boto3.session.Session()
    ec2_client = sdc_session.client('ec2', region_name='us-east-1')
    ec2_client2 = sdc_session.client('ec2', region_name='us-east-1')

    #replace this with production ec2 instances EC2_AllInstances.csv
    with open(csv_f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

		# step through each row of the csv
        for row in csv_reader:
                line_count += 1
                #For now only update the specific EC2 instance for testing purposes only
                if not ec2exist(row[0], ec2_client.describe_instances()):
                    print("Instance NOT FOUND")
                else:
                    mytags = [{"Key": "Environment", "Value": row[2]}, {"Key": "Name", "Value": row[3]},
                              {"Key": "OS", "Value": row[4]}, {"Key": "OS Release", "Value": row[5]},
                              {"Key": "Owner", "Value": row[6]}, {"Key": "Project", "Value": row[7]},
                              {"Key": "Role", "Value": row[8]}, {"Key": "Team", "Value": row[9]}]
                    print(mytags)
                    ec2_client2.create_tags(Resources=[row[0]], Tags=mytags)
                    print("EC2 updated")