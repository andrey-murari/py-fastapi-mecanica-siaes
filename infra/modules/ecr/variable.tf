variable "name" {
  type        = string
  description = "Nome do repositorio ECR, inclusive o namespace."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags do repositorio."
}
