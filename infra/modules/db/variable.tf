variable "identifier" {
  type        = string
  description = "Identificador da instancia RDS."
}

variable "db_name" {
  type        = string
  description = "Database criado junto com a instancia."
}

variable "engine_version" {
  type        = string
  description = "Versao do MySQL no RDS."
}

variable "instance_class" {
  type        = string
  description = "Classe da instancia RDS."
}

variable "username" {
  type        = string
  description = "Usuario master. Nao pode ser root."
}

variable "password" {
  type        = string
  sensitive   = true
  description = "Senha do usuario master."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnets do DB subnet group. Precisa cobrir pelo menos duas AZs."
}

variable "security_group_id" {
  type        = string
  description = "Security group que libera a porta 3306 para a API."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags da instancia e do subnet group."
}
