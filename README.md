
# CloudWatch Logs Cleanup
> Helps to reduce the clutter of your AWS CloudWatch Logs

Over the time AWS will create many log groups used by it's services like Lambda, Elastic Beanstalk etc. All of them have no retention policy set by default which means that all the log events will never expire. Depending on your usage, CloudWatch can be quite an expensive place to store the data you no longer need.

CloudWatch Logs Cleanup is a serverless solution powered by Lambda to automate CloudWatch logs management by updating the retention policy on your log groups to a configured default value.

## Features

* sets the default retention policy on a newly created log groups
* matches exact log group name
* supports prefix to narrow log group names down to a given service
* monitors log groups only in a region it was deployed to

## Deploying / Provisioning

This solution can be deployed only once per region. CloudFormation is used to provision the underlaying infrastructure.

AWS CLI installation is a prerequisite. Follow the OS specific instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)

### Create stack

Clone the project and cd into it.

```shell
git clone https://github.com/kristoka/cloudwatch-logs-cleanup.git && cd cloudwatch-logs-cleanup/
```

Make a new S3 bucket for code uploads. Run the cloudformation package command that zips the lambda_function directory, uploads it to a previously created S3 bucket and prepares a new template that references the uploaded lambda code package. 
Make sure to replace <YOUR-RANDOM-PREFIX> with something that makes this bucket name globally unique.

```shell
aws s3 mb s3://cloudwatch-logs-cleanup-code-<YOUR-RANDOM-PREFIX>
aws cloudformation package --template-file cloudwatch-logs-cleanup.yaml --s3-bucket cloudwatch-logs-cleanup-code-<YOUR-RANDOM-PREFIX> --output-template-file cloudwatch-logs-cleanup-output.yaml
```

Run the cloudformation create-stack command. It will automatically provision all the underlaying resources. Give AWS up to 10 minutes or so to fire everything up before trying it out. An S3 bucket created earlier for packaged Lambda code can be deleted after successful deployment.

```shell
aws cloudformation create-stack --stack-name cloudwatch-logs-cleanup --template-body file://cloudwatch-logs-cleanup-output.yaml --capabilities CAPABILITY_NAMED_IAM
```

### Update stack

```shell
aws cloudformation update-stack --stack-name cloudwatch-logs-cleanup --template-body file://cloudwatch-logs-cleanup-output.yaml --capabilities CAPABILITY_NAMED_IAM
```

### Delete stack

```shell
aws cloudformation delete-stack --stack-name cloudwatch-logs-cleanup
```

This will delete all the provisioned resources except these:
* CloudTrail S3 bucket named after stack e.g. cloudwatch-logs-cleanup-*
* S3 bucket created earlier for Lambda code upload

Remove them manually.

## Configuration

Configuration parameters can be provided on stack creation time or later by updating the stack.

#### RetentionInDays
Possible values: `1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653`  
Default: `30`

Used to configure the default retention period in days on a log group level.

#### LogGroupNamePrefix
Possible values: `[\\.\\-_/#A-Za-z0-9]*`  
Default: `/aws/lambda/`

Used to narrow log group names down to a given service. For an example: prefix "/aws/lambda/" will ensure that only lambda specific log groups match e.g. "/aws/lambda/FunctionName"

#### Example:
```shell
aws cloudformation update-stack --stack-name cloudwatch-logs-cleanup --template-body file://cloudwatch-logs-cleanup-output.yaml --parameters ParameterKey=RetentionInDays,ParameterValue=150 ParameterKey=LogGroupNamePrefix,ParameterValue=/aws/lambda/ --capabilities CAPABILITY_NAMED_IAM
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Licensing

The code in this project is licensed under MIT license.