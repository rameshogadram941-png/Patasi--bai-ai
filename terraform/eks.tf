# Terraform: provisioning EKS (using terraform-aws-modules/eks/aws)
# This is a recommended example. Customize node groups, CIDR ranges, and tags for production.

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  subnets         = var.subnet_ids
  vpc_id          = var.vpc_id

  manage_aws_auth = true

  # Create node groups (managed)
  node_groups = {
    default = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_types   = var.node_instance_types
      key_name         = var.ssh_key_name
    }
  }

  tags = var.common_tags

  # Enable OIDC provider creation for IRSA
  enable_irsa = true
}
