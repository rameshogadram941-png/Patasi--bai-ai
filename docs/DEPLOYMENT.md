# Deployment and setup notes for Patasi--bai-ai

This document describes how to deploy Patasi--bai-ai to AWS EKS using the provided Terraform, Helm chart, and GitHub Actions workflow.

Prerequisites
- AWS account and permissions to create ECR, EKS, IAM roles, and VPC resources.
- GitHub repository admin to configure OIDC trust and secrets.

High-level steps
1. Provision infrastructure (Terraform):
   - Configure AWS credentials locally and run `terraform init` and `terraform apply` in /terraform.
   - Terraform will create an ECR repository and (optionally) an EKS cluster if you add the module details.
2. Build & push container images:
   - The GitHub Actions workflow uses OIDC to assume an IAM role (recommended). Create an OIDC role in AWS and allow GitHub Actions to assume it. Set the role ARN in the repository secret AWS_AOIDC_ROLE (or use secrets.AWS_ACCOUNT_ID and create a role name as used in the workflow).
3. Deploy to EKS with Helm:
   - The workflow runs helm upgrade --install to deploy the chart in /helm.

Required GitHub secrets (recommended):
- AWS_ACCOUNT_ID: your AWS account id
- AWS_REGION: e.g. us-east-1
- EKS_CLUSTER_NAME: name of your EKS cluster
- (Optional fallback) AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

OIDC setup (summary):
1. In AWS IAM, create a role for Web Identity with provider https://token.actions.githubusercontent.com and trust policy for your repo or org.
2. Attach permissions: ECR (push/pull), EKS (update-kubeconfig), and any other IAM managed policies you need.
3. In GitHub, no secret is needed for OIDC; ensure the workflow requests id-token: write permission.

Next steps / TODOs:
- Add a complete Terraform EKS module (recommend: https://github.com/terraform-aws-modules/terraform-aws-eks)
- Harden IAM roles and least-privilege policies
- Enable ALB Ingress Controller / AWS Load Balancer Controller if you need Ingress + ALB
- Add secrets management (ExternalSecrets or AWS Secrets Manager) and IRSA mappings
