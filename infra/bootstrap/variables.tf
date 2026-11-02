variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Regiao do bucket de state. A mesma de infra/backend.tf."
}

variable "bucket_name" {
  type        = string
  default     = "mecanica-tfstate-336586907022"
  description = "Bucket do state remoto. Mantenha igual ao bucket em infra/backend.tf."
}
