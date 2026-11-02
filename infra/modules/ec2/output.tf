output "instance_id" {
  description = "ID da instancia."
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "IP elastico da API."
  value       = aws_eip.this.public_ip
}

output "security_group_ids" {
  description = "Security groups anexados a instancia."
  value       = aws_instance.this.vpc_security_group_ids
}
