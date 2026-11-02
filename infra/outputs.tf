output "api_url" {
  description = "Documentacao da API."
  value       = "http://${module.ec2.public_ip}:8000/docs"
}

output "ec2_instance_id" {
  description = "Instancia que executa o container."
  value       = module.ec2.instance_id
}

output "ecr_repository_url" {
  description = "URL do repositorio ECR, sem a tag."
  value       = module.ecr.repository_url
}

output "mysql_host" {
  description = "Endpoint do RDS, sem a porta."
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
