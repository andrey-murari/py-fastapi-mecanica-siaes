variable "name" {
  type        = string
  description = "Nome da role, do instance profile e base da tag Name."
}

variable "ami" {
  type        = string
  description = "AMI da instancia."
}

variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "Tipo da instancia."
}

variable "subnet_id" {
  type        = string
  description = "Subnet publica da VPC default."
}

variable "vpc_security_group_ids" {
  type        = list(string)
  description = "Security groups da instancia."
}

variable "user_data" {
  type        = string
  sensitive   = true
  description = "Script de boot que sobe o container da API."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags da instancia, da role e do EIP."
}
