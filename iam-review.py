import boto3
import csv

# Create a boto3 IAM client with access key ID and secret access key
client = boto3.client('iam', aws_access_key_id="", aws_secret_access_key="")

# Get the list of IAM users
response = client.list_users()

# Open a CSV file to write the policy data
with open('user-policies.csv', mode='w') as csv_file:
    fieldnames = ['UserName', 'PolicyName']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over the list of IAM users
    for user in response['Users']:
        # Get the name of the user
        user_name = user['UserName']

        # Get the list of policy names attached directly to the user
        response = client.list_user_policies(UserName=user_name)

        # Iterate over the list of policy names and write the policy name and username to the CSV file
        for policy_name in response['PolicyNames']:
            writer.writerow({'UserName': user_name, 'PolicyName': policy_name})

        # Get the list of policy names attached to the user's groups
        response = client.list_groups_for_user(UserName=user_name)

        # Iterate over the list of groups and get the list of policies attached to each group
        for group in response['Groups']:
            group_name = group['GroupName']

            # Get the list of policy names attached to the group
            response = client.list_attached_group_policies(GroupName=group_name)

            # Iterate over the list of policy names and write the policy name and username to the CSV file
            for policy in response['AttachedPolicies']:
                writer.writerow({'UserName': user_name, 'PolicyName': policy['PolicyName']})

        # Get the list of policy names attached to the user
        response = client.list_attached_user_policies(UserName=user_name)

        # Iterate over the list of policy names and write the policy name and username to the CSV file
        for policy in response['AttachedPolicies']:
            writer.writerow({'UserName': user_name, 'PolicyName': policy['PolicyName']})
