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
        print("Splitting...")
        if file_exists(args.file):
            print(f"File '{args.file}' exists. Spitting....")
            
            # Run a command and capture its output
            result = subprocess.run(['split', '-d', '-b', str(args.chunk), str(args.file), str(args.file)+'.part'], capture_output=True, text=True)

            # Check if the command was successful
            if result.returncode == 0:
                print("Splitting files done....sending to diode")



            else:
                print("Split failed with error:")
                print(result.stderr)
    else:
        print(f"AWS Account is not configured ")