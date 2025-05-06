# send2S3
This script takes in a file from command line input, splits it into many parts, then sends to an S3 bucket.

## Requirements
1) AWS CLI installed and configured: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html 
2) boto3 python library: https://pypi.org/project/boto3/
3) S3 bucket must already exsist 
4) IAP permissions to write to S3

#### Command Line Arugments 
-f, -file: full path of the file to split and send to S3
-c, -chunks: size of the file parts; i.e. 100m for 100 MB
-b, -bucket: AWS bucket name

## Usage
```
python3 send2S3.py -f example/file/name.exe -c 100m -b example-s3-bucket
```