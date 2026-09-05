# Terraform outputs for EKS
output "cluster_id" {
  description = "EKS cluster id"
  value       = module.eks.cluster_id
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_certificate_authority_data" {
  value = module.eks.cluster_certificate_authority_data
}

output "kubeconfig" {
  description = "Kubeconfig (base64 encoded)"
  value       = module.eks.kubeconfig
  sensitive   = true
}
