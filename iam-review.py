import boto3
import csv

client = boto3.client('iam', aws_access_key_id="", aws_secret_access_key="")

response = client.list_users()

with open('user-policies.csv', mode='w') as csv_file:
    fieldnames = ['UserName', 'PolicyName']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for user in response['Users']:
        user_name = user['UserName']

        response = client.list_user_policies(UserName=user_name)

        for policy_name in response['PolicyNames']:
            writer.writerow({'UserName': user_name, 'PolicyName': policy_name})

        response = client.list_groups_for_user(UserName=user_name)

        for group in response['Groups']:
            group_name = group['GroupName']

            response = client.list_attached_group_policies(GroupName=group_name)

            for policy in response['AttachedPolicies']:
                writer.writerow({'UserName': user_name, 'PolicyName': policy['PolicyName']})

        response = client.list_attached_user_policies(UserName=user_name)

        for policy in response['AttachedPolicies']:
            writer.writerow({'UserName': user_name, 'PolicyName': policy['PolicyName']})
