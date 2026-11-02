output "bucket_name" {
  description = "Bucket usado em infra/backend.tf."
  value       = module.tfstate.bucket_name
}

output "bucket_arn" {
  description = "ARN do bucket de state."
  value       = module.tfstate.bucket_arn
}
