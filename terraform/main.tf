# Terraform root (scaffold) - AWS provider and example module calls
terraform {
  required_version = ">= 1.1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# ECR repository
resource "aws_ecr_repository" "patasi" {
  name = "patasi-bai-ai"
  image_scanning_configuration { scan_on_push = true }
}

# Note: for EKS, use the eks module or provide your own. This is a scaffold.
# See modules/eks/ for a recommended module implementation.

output "ecr_repository_url" {
  value = aws_ecr_repository.patasi.repository_url
}
