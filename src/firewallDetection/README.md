# Function:

This folder is used to test whether there is a firewall or middlebox that limits DNS request between some networks. 'aws_scan_client.py' is used to query and 'aws_scan_server.py' is used to receive packets and do statistics.

##  To access your instance:

1. Open an SSH client. (find out how to connect using PuTTY)


2. Locate your private key file (AWS_1.pem). The wizard automatically detects the key you used to launch the instance.


3. Your key must not be publicly viewable for SSH to work. Use this command if needed:

```bash
 chmod 400 AWS_1.pem
```

4. Connect to your instance using its Public DNS:

```bash 
ec2-18-188-87-197.us-east-2.compute.amazonaws.com
```

## Example:

```bash
ssh -i "AWS_1.pem" ubuntu@ec2-18-188-87-197.us-east-2.compute.amazonaws.com
```

Please note that in most cases the username above will be correct, however please ensure that you read your AMI usage instructions to ensure that the AMI owner has not changed the default AMI username.