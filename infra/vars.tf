variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Regiao AWS. A imagem do CI tambem e publicada em us-east-1."
}

variable "environment" {
  type        = string
  default     = "develop"
  description = "Valor da tag Environment."
}

variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "Tipo da instancia EC2 que executa o container da API."
}

variable "api_ingress_cidr" {
  type        = string
  default     = "0.0.0.0/0"
  description = "CIDR liberado para acessar a API na porta 8000."
}

variable "ecr_repository_name" {
  type        = string
  default     = "fiap-17soat/siaes-ci-cd"
  description = "Repositorio ECR. O mesmo nome usado em .github/workflows/ci-multistage.yml."
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Tag da imagem que a EC2 puxa do ECR."
}

variable "mysql_database" {
  type        = string
  default     = "siae"
  description = "Database inicial do RDS. A API le MYSQL_DATABASE."
}

variable "mysql_user" {
  type        = string
  default     = "siae"
  description = "Usuario master do RDS e MYSQL_USER da API. O RDS nao aceita root."

  validation {
    condition     = var.mysql_user != "root" && length(var.mysql_user) > 0
    error_message = "Informe um usuario MySQL diferente de root."
  }
}

variable "mysql_password" {
  type        = string
  sensitive   = true
  description = "Senha do MySQL. Passe por TF_VAR_mysql_password ou terraform.tfvars (nao versionado)."

  validation {
    condition = (
      length(var.mysql_password) >= 8 &&
      length(var.mysql_password) <= 41 &&
      length(regexall("[/'\"@ \\r\\n]", var.mysql_password)) == 0
    )
    error_message = "Senha do MySQL: 8 a 41 caracteres, sem espaco, aspas, barra ou @."
  }
}

variable "mysql_engine_version" {
  type        = string
  default     = "8.4.11"
  description = "Versao do MySQL no RDS. A 9.7 do Compose so existe no RDS Preview; em producao a linha suportada e a 8.4."
}

variable "db_instance_class" {
  type        = string
  default     = "db.t3.micro"
  description = "Classe da instancia RDS."
}

variable "jwt_secret" {
  type        = string
  sensitive   = true
  description = "JWT_SECRET da API. Passe por TF_VAR_jwt_secret ou terraform.tfvars (nao versionado)."

  validation {
    condition     = length(var.jwt_secret) >= 16 && length(regexall("[\\r\\n]", var.jwt_secret)) == 0
    error_message = "JWT_SECRET precisa ter pelo menos 16 caracteres e nao pode ter quebra de linha."
  }
}

variable "admin_login" {
  type        = string
  default     = "admin"
  description = "ADMIN_LOGIN da API."

  validation {
    condition     = length(var.admin_login) > 0 && length(regexall("[\\r\\n]", var.admin_login)) == 0
    error_message = "ADMIN_LOGIN nao pode ser vazio nem conter quebra de linha."
  }
}

variable "admin_password" {
  type        = string
  sensitive   = true
  description = "ADMIN_PASSWORD da API. Passe por TF_VAR_admin_password ou terraform.tfvars (nao versionado)."

  validation {
    condition     = length(var.admin_password) > 0 && length(regexall("[\\r\\n]", var.admin_password)) == 0
    error_message = "ADMIN_PASSWORD nao pode ser vazio nem conter quebra de linha."
  }
}
