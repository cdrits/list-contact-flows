import json
import boto3
import botocore
import os

INSTANCE_ID = os.environ['INSTANCE_ID'] # The Amazon connect INSTANCE_ID (environment variable)
BUCKET_NAME = os.environ['BUCKET_NAME '] # The S3 BUCKET_NAME (environment variable)
prefix = os.environ['prefix'] # S3 object prefix

# Clients for Amazon Connect and S3

connect_client = boto3.client('connect')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    cfstr = fetch_contact_flows()
    result = write_to_s3(cfstr)

    return {
        'body': str(result)
    }

def fetch_contact_flows():
    contact_flow_list = connect_client.list_contact_flows(InstanceId=INSTANCE_ID, ContactFlowTypes = ['CONTACT_FLOW'])
    cfstr = 'Name, Arn \n'

    for index in range(len(contact_flow_list['ContactFlowSummaryList'])):
        cfstr += contact_flow_list['ContactFlowSummaryList'][index]['Name'] + ', ' + contact_flow_list['ContactFlowSummaryList'][index]['Arn'] + "\n"

        print(str(len(contact_flow_list['ContactFlowSummaryList'])) + ' contact flows found.')

    return cfstr

# Write datastring to S3 bucket
def write_to_s3(datastring):
    try:
        s3_client.put_object(Bucket = BUCKET_NAME, Key = prefix + '/' + 'list-contact-flows.csv', Body = datastring)
        result = 'The QuickConnect data was written to: ' + BUCKET_NAME + '/' + prefix
    except botocore.exceptions.ClientError as error:
        print(error)
        result = str(error)

    return result