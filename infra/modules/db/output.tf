output "address" {
  description = "Hostname do RDS."
  value       = aws_db_instance.this.address
}

output "port" {
  description = "Porta do MySQL."
  value       = aws_db_instance.this.port
}

output "db_name" {
  description = "Database inicial."
  value       = aws_db_instance.this.db_name
}
