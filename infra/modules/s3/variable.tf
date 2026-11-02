variable "bucket_name" {
  type        = string
  description = "Nome global do bucket."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags do bucket."
}
