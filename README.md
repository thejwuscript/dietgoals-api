# DietGoals API

This is the serverless backend of the app, built with AWS services.

[Frontend repo](https://github.com/thejwuscript/dietgoals)

## Architecture Overview

![DietGoals Backend Architecture](https://github.com/thejwuscript/dietgoals-api/assets/88938117/c422632e-5156-44cf-bc28-d2a12d775f7d)


### Services Used

1. **Amazon CloudFront**: A content delivery network (CDN) that distributes API requests to the nearest Point of Presence, thereby reducing latency for clients around the world.
2. **AWS** **Certificate Manager**: Provides TLS/SSL certificate for HTTPS connection.
3. **Amazon** **API Gateway**: A centralized entry point for applications to connect to backend services.
4. **AWS Lambda**: A serverless computing service that executes code in response to events. In this application, it responds to events coming from API Gateway.
5. **Amazon** **DynamoDB**: A fully managed NoSQL database service.
6. **AWS CloudFormation**: Allows developers to define and provision AWS infrastructure as code.
7. **AWS IAM**: Manages access to AWS resources by creating policies and attaching them to IAM identities.
8. **Amazon CloudWatch:** Provides monitoring and logging services for AWS resources.
9. **DNS Hosting**: A service that points a custom domain name to an IP address or another domain name. A cost-effective alternative to Route 53 is used for this app.
10. **GitHub Actions**: A CI/CD platform that allows developers to automate build, test, and deployment tasks.
