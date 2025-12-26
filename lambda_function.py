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
users = [
    {"username" : "alice",
     "userid" : "U12345",
     "role" : "Admin",
     "created":"2024-01-01"},
     
     {"username" : "bob",
      "userid" : "U12346",
      "role" : "ReadOnly",
      "created":"2023-06-15"},
      
      {"username" : "carol",
       "userid" : "U12347",
       "role" : "Developer",
       "created":"2023-12-10"}]

roles = [
    {"role" : "Admin",
     "permissions" : ["*"],
     "description" : "Full access to services"},
     
     {"role" : "ReadOnly",
     "permissions" : ["s3:GetObject", "ec2:DescribeInstances"],
     "description" : "Read-only access"},
      
      {"role" : "Developer",
     "permissions" : [" s3:*, lambda:InvokeFunction"],
     "description" : "Developer access"},]

policy = [
    {"username" : "bob",
     "policyname" : "ExtraS3Access",
     "permissions" : ["s3:PutObject"]},
     
     {"username" : "carol ",
     "policyname" : "LimitedEC2",
     "permissions" : ["ec2:StartInstances, ec2:StopInstances"]},]


#organize in structured JSON
#call function 

def lambda_handle(event, context):
    #return all IAM as structured dictionary 
    return {
        "Users": users,
        "Roles": roles,
        "Policies": policy
    }

#return mock data as dict


response = lambda_handle({}, None)
print(response)