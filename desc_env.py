
"""
Base command parsing
"""
import configobj
import sys
import os
import argparse
import hashlib
import base64
import botocore.session
import json
from botocore.exceptions import ClientError


def print_json(obj):
    print json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))


def print_count(service, response, path):
    print service + " " + str(len(response[path]))


def service_objects(obj, *args, **kw):
    pass


if __name__ == "__main__":
    credentials = "~/.aws/credentials"
    profile = "cco-dev-test:LasanthaR"
    #profile= "LasanthaR-dev-test"
    #profile= "ebuilder-prod-eu-west"

    if not os.path.exists(os.path.expanduser(credentials)):
        raise argparse.ArgumentError(
            'The specified credentials file does not exist')

    cred = configobj.ConfigObj(os.path.expanduser(credentials))

    if profile not in cred:
        raise argparse.ArgumentError(
            'The specified profile "%s" does not exist in the credentials file.' %
            (profile,))

    region = cred[profile].get('region', None)

    for key in ('aws_access_key_id', 'aws_secret_access_key'):
        if key not in cred[profile]:
            raise argparse.ArgumentError(
                self, 'The specified profile does not define the parameter "%s"' %
                (key,))

    aws_id = cred[profile]['aws_access_key_id']
    aws_key = cred[profile]['aws_secret_access_key']

    region = "eu-west-1"

    session = botocore.session.get_session()

    # Add what ever service you want to test here
    service_list = {
        's3': 'list_buckets',
        'lambda': 'list_functions',
        'acm': 'list_certificates'}

    service_count_path = {
        's3': 'Buckets',
        'lambda': 'Functions',
        'acm': 'CertificateSummaryList'}

    #service_list = {'ec2': 'describe_instances'}
    # service_count_path = {
    #    's3': 'Buckets',
    #    'lambda': 'Functions',
    #    'ec2': 'Instances'}

    for service in service_list.keys():
        client = session.create_client(
            service_name=service,
            aws_access_key_id=aws_id,
            aws_secret_access_key=aws_key,
            region_name=region)

        try:
            method = getattr(client, service_list[service])
            response = method()
            print_count(service, response, service_count_path[service])
        except:
            print service+" -> No access"
