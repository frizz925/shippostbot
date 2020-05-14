terraform {
  backend "s3" {
    bucket = "kogane-terraform-states"
    key    = "shippostbot/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

provider "aws" {
  region = "${var.aws_region}"
}
