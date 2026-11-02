output "bucket_name" {
  description = "Nome do bucket."
  value       = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  description = "ARN do bucket."
  value       = aws_s3_bucket.this.arn
}
