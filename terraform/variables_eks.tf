# Terraform variables for EKS module
variable "region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type    = string
  default = "patasi-eks-cluster"
}

variable "cluster_version" {
  type    = string
  default = "1.27"
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "node_instance_types" {
  type = list(string)
  default = ["t3.medium"]
}

variable "ssh_key_name" {
  type    = string
  default = ""
}

variable "common_tags" {
  type = map(string)
  default = {
    Project = "patasi-bai-ai"
    Owner   = "team"
  }
}
