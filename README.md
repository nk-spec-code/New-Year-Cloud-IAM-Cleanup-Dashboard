if New_Year == New_Me OR True #Even IF conjunction is True 

# AWS IAM Risk Analyzer Dashboard
A serverless security dashboard that scans an AWS account’s IAM configuration to identify:

- Overly permissive policies (* or service:*)
- High-risk access patterns  
- Unused users and roles  
- Least-privilege recommendations  

This is revealed through a secure IAM API and is displayed on a browser-based dashboard.



## Project vs. AWS Native

AWS provides raw IAM data and some access analysis, but it does not offer a unified dashboard with high-risk classification, least-privilege recommendations, charts, or cleanup summaries - which this project implements.



## Architecture

Serverless, fully managed AWS stack:

| Component | Purpose |
|---------|---------|
| AWS Lambda | Core IAM analysis |
| AWS IAM | Read-only access |
| Amazon API Gateway (HTTP API) | Secure API |
| CloudWatch Logs | Debugging |
| Static Frontend (HTML + JS) | Dashboard UI |
| Chart.js | Risk visualization |

**Flow:**

Browser > API Gateway (HTTPS) > Lambda (IAM Analyzer) > AWS IAM (Read-Only)

## How The Analyzer Detects

### High Risk Policies

A policy is considered and flagged HIGH risk and not least-privilege if it includes:

- Action: “”  
- Service: * (e.g, for logs: *, iam:*)  
- Resource: “*”



### Least-Privilege Recommendations

For each risky (med to high) risk policy, a suggestion is made regarding:

- Restricting wildcard actions  
- Limiting resources to specific ARNs  
- Narrowing scope to specific services  

E.g Restrict 'logs:*' to specific actions and resources ["*"]



### Unused identities

Identifies:

- Users with no attached policies  
- Roles with no attached policies  

Candidates for cleanup to reduce attack surface.



## Dashboard Features

- Doughnut chart showing High/Low risk policies  
- Interactive Filters to filter out high risk, user only, role only  
- Live search: search by username, role or policy name  
- Cleanup: count of unused users and roles  
- Clear risk labels and recommendations  


## Security & Design Choices

- Uses IAMReadOnlyAccess only  
- No AWS credentials stored in the frontend, uses config.js  
- API Gateway endpoint exposes data only, no control  
- CORS configured for frontend access  
- Lambda role principle-of-least-privilege enforced  


## Instructions

Clone the repo, create a config.js with your API Gateway URL, and open index.html in a browser (served via local web server) to view the dashboard.

