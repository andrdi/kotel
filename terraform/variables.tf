variable "availability_zone" {
  type = string
  default = "eu-central-1"
}

variable profile {
  description = "Profile"
  default = "AWS-user"
}

variable "access_key" {
  type = string
  default = "my-access-key"
}

variable "secret_key" {
  type = string
  default = "my-secret-key"
}
