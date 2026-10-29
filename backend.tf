terraform {
  backend "s3" {
    bucket = "mecanica-tfstate-backend"
    key    = "mecanica/2026/terraform.tfstate"
    region = "us-east-1"
  }
}
