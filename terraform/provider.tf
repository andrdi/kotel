terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region     = var.availability_zone
  profile    = var.profile
  access_key = var.access_key
  secret_key = var.secret_key
}
