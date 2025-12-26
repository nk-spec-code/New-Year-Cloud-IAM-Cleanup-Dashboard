import boto3

iam = boto3.client("iam")
users = iam.list_users()

"""Input: “Give me IAM data”
Function: Looks at fake data, 

list of users list_users()
list of roles list_roles()
policies attached to a role
full JSON of a policy get_policy()


Output: Returns structured JSON

Users:
  - UserName
  - Role(s)
  - Policies
Roles:
  - RoleName
  - Policies
Policies:
  - PolicyName
  - Permissions

Can ask for users, roles, policies 

"""


#organize in structured JSON
#call function 

def lambda_handle(event, context):
    #return all IAM as structured dictionary 
    users_response = iam.list_users()
    users = []

    for i in users_response["Users"]:
        users.append({
            "username":i.get("UserName"),
            "userid":i.get("UserId"),
            "createdate":i.get("CreateDate"),
            "arn":i.get("Arn"),
            })
    
    roles_response = iam.list_roles()
    roles = []

    for x in roles_response["Roles"]:
        roles.append({
            "rolename":x.get("RoleName"),
            "arn":x.get("Arn"),
            "createdate":str(x.get("CreateDate"))
        })
    
    policies =[]

    for u in users:
      attached_policies = iam.list_attached_user_policies(
        UserName=u["username"]
    )["AttachedPolicies"]

      for p in attached_policies:
        policies.append({
            "username": u["username"],
            "policyname": p.get("PolicyName"),
            "policyarn": p.get("PolicyArn"),
        })
    for r in roles:
       attached_policies = iam.list_attached_role_policies(
        RoleName=r["rolename"]
    )["AttachedPolicies"]

       for p in attached_policies:
             policies.append({
            "rolename": r["rolename"],
            "policyname": p.get("PolicyName"),
            "policyarn": p.get("PolicyArn"),
            })

    return {
        "Users": users,
        "Roles": roles,
        "Policies": policies}

#return mock data as dict


response = lambda_handle({}, None)
print(response)


