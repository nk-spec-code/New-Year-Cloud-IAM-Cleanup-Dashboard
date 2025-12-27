import boto3

iam = boto3.client("iam")

def get_permissions(policy_arn):
    policy = iam.get_policy(PolicyArn=policy_arn)
    version_id = policy["Policy"]["DefaultVersionId"]
    policy_version = iam.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)
    return policy_version["PolicyVersion"]["Document"]

def is_policy_high_risk(policy_document):
    statements = policy_document.get("Statement", [])

    if not isinstance(statements, list):
        statements = [statements]

    for s in statements:
        actions = s.get("Action", [])

        if isinstance(actions, str):
            actions = [actions]

        for action in actions:
            if action == "*" or action.endswith(":*"):# 
                return True
    return False
