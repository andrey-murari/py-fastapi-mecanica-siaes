# Estado remoto do stack da API.
# O bucket nasce em infra/bootstrap e precisa existir antes do init.
# O nome abaixo tem de ser o mesmo de bucket_name no bootstrap.
terraform {
  backend "s3" {
    bucket       = "mecanica-tfstate-336586907022"
    key          = "mecanica/2026/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
