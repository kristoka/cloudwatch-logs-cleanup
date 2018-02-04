from __future__ import print_function

import boto3
from os import environ

logs = boto3.client('logs')

def lambda_handler(event, context):

  log_group_name = event['detail']['requestParameters']['logGroupName']
  retention_in_days = int(environ['retention_in_days'])
  log_group_prefix = environ.get('log_group_prefix', '').strip()

  response = logs.describe_log_groups(
    logGroupNamePrefix=log_group_name
  )
  
  for logGroup in response['logGroups']:
    if not logGroup['logGroupName'].startswith(log_group_prefix):
      continue
    if logGroup['logGroupName'] != log_group_name:
      continue
    if 'retentionInDays' not in logGroup:
      logs.put_retention_policy(
        logGroupName=log_group_name,
        retentionInDays=retention_in_days
      )
      print('Updated retention policy to {} days for log group {}.'.format(retention_in_days, log_group_name))
      break

  return 'Done'
