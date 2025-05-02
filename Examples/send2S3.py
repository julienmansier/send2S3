import argparse
import os
import subprocess
import boto3


def is_aws_configured(profile_name=None):
    try:
        # Create a session, optionally using a named profile
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
        else:
            session = boto3.Session()
        
        # Use STS to get caller identity (safe, no permissions needed except valid credentials)
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        
        print("AWS account is configured.")
        print(f"Account: {identity['Account']}")
        print(f"UserId: {identity['UserId']}")
        print(f"ARN: {identity['Arn']}")
        return True
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found or incomplete.")
        return False
    except ClientError as e:
        print(f"Failed to validate AWS credentials: {e}")
        return False
    

def bucket_exists(bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' exists and is accessible.")
        return True
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print(f"Bucket '{bucket_name}' does not exist.")
        else:
            print(f"Error accessing bucket '{bucket_name}': {e}")
        return False




def file_exists(filepath):
    """Check if the file exists at the given filepath."""
    return os.path.isfile(filepath)

def parse_args():
    parser = argparse.ArgumentParser(description='Process a file with park or unpack options.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the file')
    parser.add_argument('-c', '--chunk', type=str, help='Chunk size')
    parser.add_argument('-d', '--diode', type=str, help='Chunk size')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if is_aws_configured():
        print("AWS Account Configured. Splitting...")
        if file_exists(args.file):
            print(f"File '{args.file}' exists. Spitting....")
            
            # Run a command and capture its output
            result = subprocess.run(['split', '-d', '-b', str(args.chunk), str(args.file), str(args.file)+'.part'], capture_output=True, text=True)

            # Check if the command was successful
            if result.returncode == 0:
                print("Splitting files done....sending to diode")

                bucket_name =str(args.diode)
                if bucket_exists(bucket_name):
                    print("Bucket exists. Sending...")
                    s3_client = boto3.client('s3')

                    for filename in os.listdir('.'):
                        # Check if the item is a file and contains '.part' in its name
                        if os.path.isfile(filename) and '.part' in filename:
                            try:
                                s3_client.upload_file(filename, str(args.diode), filename)
                                print(f"File uploaded successfully to s3://{bucket_name}/{filename}")
                            except Exception as e:
                                print(f"Error uploading file: {e}")
                else:
                    print("Bucket does not exist or is not accessible.")

            else:
                print("Split failed with error:")
                print(result.stderr)
        else:
            print("File not found!")
    else:
        print(f"AWS Account is not configured ")