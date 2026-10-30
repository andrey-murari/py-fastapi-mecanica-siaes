variable "mysql_password" {
  type        = string
  sensitive   = true
  description = "Senha do banco de dados MySQL"
}

variable "tags_dev" {
  type = map(any)
  default = {
    name        = "mecanica"
    environment = "develop"
  }
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}