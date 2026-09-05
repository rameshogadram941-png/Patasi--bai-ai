IAM OIDC role trust policy and permission policy for GitHub Actions

Follow these steps in AWS IAM (or use Terraform):

1) Create an IAM OIDC provider for your account if not created already. The terraform-aws-eks module can create it for the cluster when enable_irsa = true.

2) Create a role with WebIdentity trust relationship to token.actions.githubusercontent.com. Use a condition to limit which repo/org can assume the role. Example trust policy (replace OWNER/REPO):

Trust policy (github-oidc-trust.json):
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USER_OR_ORG/YOUR_REPO:*"
        }
      }
    }
  ]
}

3) Attach a least-privilege inline policy for CI/CD that allows ECR push/pull and EKS describe + update-kubeconfig actions. Example permission policy (github-actions-oidc-policy.json):
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRPushPull",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Sid": "EKSDescribe",
      "Effect": "Allow",
      "Action": [
        "eks:DescribeCluster"
      ],
      "Resource": "arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}"
    }
  ]
}

Notes:
- You can scope ECR actions to a specific repository ARN instead of "*" for tighter security.
- If you use AWS SSM / Parameter Store or Secrets Manager in the workflow, add read access to those resources.
- For advanced flows (creating node groups or managing IAM), consider separate roles with narrower permissions.
