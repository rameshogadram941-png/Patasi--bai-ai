PR: infra/eks-ecr-helm-cicd -> main

What this PR includes:
- Full scaffolding for deploying Patasi--bai-ai to AWS EKS
  - Dockerfile and minimal FastAPI app
  - Helm chart + values for OpenAI/Stripe/DB
  - Terraform scaffold extended to include terraform-aws-modules/eks/aws usage
  - OpenAI/Codex integration endpoints and usage metering
  - CI workflow using GitHub OIDC to push images to ECR and deploy via helm
  - IAM guidance for creating the OIDC role and least-privilege policy

How to review:
1. Inspect terraform/ for the eks module usage and variables. Provide VPC/subnet IDs before running terraform apply.
2. Review docs/IAM_OIDC.md for instructions to set up GitHub OIDC trust and policies.
3. Verify helm/values.yaml and values-openai.yaml for placeholders: update <AWS_ACCOUNT_ID> and region.
4. Run the app locally with DATABASE_URL and OPENAI_API_KEY set to test endpoints.

Manual steps required before merge:
- Create or provide a VPC and subnet IDs and set terraform variables for vpc_id and subnet_ids, or expand the terraform to create a VPC.
- Create GitHub OIDC role in AWS and add the role ARN to the GitHub Actions workflow secrets or update workflow to use the role-to-assume directly.
- Add secrets to GitHub: AWS_ACCOUNT_ID, AWS_REGION, EKS_CLUSTER_NAME, OPENAI_API_KEY, STRIPE_SECRET_KEY, DATABASE_URL.

If you want, I can now:
- Expand terraform to create VPC + subnets automatically (I can add this module),
- Create a more restrictive IAM policy scoping ECR to the created repo,
- Draft the exact AWS CLI / Terraform commands to create the OIDC role and attach the policy.
