variable "tags" {
  default = {}
}

variable "cidr_block" {
  default = "10.4.0.0/16"
}

variable "region" {
  default = "eu-central-1"
}

variable "additional_ip_addresses" {
  type        = list(string)
  default     = []
  description = "Additional IP addresses or rangees from which access to the VM will happen."
}

