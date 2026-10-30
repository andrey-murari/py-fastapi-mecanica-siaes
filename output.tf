output "bucket-arn" {
    value = aws_s3_bucket.mecanica-tfstate-backend.arn
}

output "bucket-acl" {
    value = aws_s3_bucket.mecanica-tfstate-backend.acl
}