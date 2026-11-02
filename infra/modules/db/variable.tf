variable "identifier" {
  type        = string
  description = "Identificador da instancia RDS."
}

variable "db_name" {
  type        = string
  description = "Database criado junto com a instancia."
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
  description = "Security group que libera a porta 3306."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags da instancia e do subnet group."
}
