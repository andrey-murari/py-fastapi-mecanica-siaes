resource "aws_s3_bucket" "mecanica-tfstate-backend" {
  bucket = "mecanica-tfstate-backend"

  tags = {
    Name        = "Mecanica Terraform tfstate Bucket"
    Environment = "Production"
  }
}
