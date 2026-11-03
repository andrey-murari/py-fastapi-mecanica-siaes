output "ecr_repository_url" {
  description = "URL do repositorio ECR, sem a tag."
  value       = aws_ecr_repository.this.repository_url
}

output "cluster_name" {
  description = "Nome do cluster EKS."
  value       = aws_eks_cluster.this.name
}

output "cluster_endpoint" {
  description = "Endpoint publico da API do Kubernetes."
  value       = aws_eks_cluster.this.endpoint
}

output "kubeconfig_command" {
  description = "Aponta o kubectl para este cluster. Use o mesmo usuario IAM que rodou o terraform."
  value       = "aws eks update-kubeconfig --region ${var.region} --name ${aws_eks_cluster.this.name}"
}

output "mysql_host" {
  description = "Endpoint publico do RDS, sem a porta."
  value       = module.db.address
}

output "mysql_port" {
  description = "Porta do MySQL."
  value       = module.db.port
}

output "mysql_database" {
  description = "Database criado no RDS."
  value       = module.db.db_name
}

output "mysql_user" {
  description = "Usuario master do MySQL."
  value       = var.mysql_user
}
