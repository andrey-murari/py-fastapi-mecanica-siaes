variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Regiao AWS. O Learner Lab usa us-east-1."
}

variable "mysql_database" {
  type        = string
  default     = "siae"
  description = "Database inicial do RDS."
}

variable "mysql_user" {
  type        = string
  default     = "siae"
  description = "Usuario master do RDS. O RDS nao aceita root."

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
