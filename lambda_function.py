import boto3
import json

iam = boto3.client("iam")

def get_permissions(policy_arn):
    version = iam.get_policy(PolicyArn=policy_arn)["Policy"]["DefaultVersionId"]
    return iam.get_policy_version(
        PolicyArn=policy_arn,
        VersionId=version
    )["PolicyVersion"]["Document"]

def classify_policy_risk(policy_name, policy_doc):
    statements = policy_doc.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]

    for s in statements:
        action = s.get("Action", [])
        resource = s.get("Resource", [])
        if action == "*" or resource == "*":
            return "HIGH"
        if isinstance(action, list) and any(a == "*" or a.endswith(":*") for a in action):
            return "HIGH"

    if "FullAccess" in policy_name or "ReadOnly" in policy_name:
        return "MEDIUM"

    return "LOW"

def recommend_least_privilege(policy_doc):
    statements = policy_doc.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]

    suggestions = []

    for s in statements:
        actions = s.get("Action", [])
        resources = s.get("Resource", [])
        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]

        for action in actions:
            if action == "*" or action.endswith(":*"):
                suggestions.append(
                    f"Restrict '{action}' to specific actions and resources {resources}"
                )

    return suggestions

def lambda_handler(event, context):
    users_data = []
    roles_data = []
    policies = []

    users = iam.list_users()["Users"]
    roles = iam.list_roles()["Roles"]

    for u in users:
        attached = iam.list_attached_user_policies(UserName=u["UserName"])["AttachedPolicies"]
        unused = len(attached) == 0

        users_data.append({
            "username": u["UserName"],
            "createdate": u["CreateDate"].isoformat(),
            "unused": unused
        })

        for p in attached:
            policy_doc = get_permissions(p["PolicyArn"])
            risk = classify_policy_risk(p["PolicyName"], policy_doc)
            recommendations = recommend_least_privilege(policy_doc)

            policies.append({
                "attached_to": u["UserName"],
                "type": "user",
                "policyname": p["PolicyName"],
                "policyarn": p["PolicyArn"],
                "risk_level": risk,
                "high_risk": risk == "HIGH",
                "recommendations": recommendations
            })

    for r in roles:
        attached = iam.list_attached_role_policies(RoleName=r["RoleName"])["AttachedPolicies"]
        unused = len(attached) == 0

        roles_data.append({
            "rolename": r["RoleName"],
            "createdate": r["CreateDate"].isoformat(),
            "unused": unused
        })

        for p in attached:
            policy_doc = get_permissions(p["PolicyArn"])
            risk = classify_policy_risk(p["PolicyName"], policy_doc)
            recommendations = recommend_least_privilege(policy_doc)

            policies.append({
                "attached_to": r["RoleName"],
                "type": "role",
                "policyname": p["PolicyName"],
                "policyarn": p["PolicyArn"],
                "risk_level": risk,
                "high_risk": risk == "HIGH",
                "recommendations": recommendations
            })

    response = {
        "Users": users_data,
        "Roles": roles_data,
        "Policies": policies,
        "CleanupSummary": {
            "unused_users": [u["username"] for u in users_data if u["unused"]],
            "unused_roles": [r["rolename"] for r in roles_data if r["unused"]]
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response)
    }
