resource "aws_s3_bucket" "mecanica-tfstate-backend" {
  bucket = "mecanica-tfstate-backend"
  tags   = var.tags_dev
}
