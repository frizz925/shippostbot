variable "facebook_access_token" {
  type = "string"
}

variable "s3_bucket_name" {
  type = "string"
  default = "shippostbot"
}

variable "aws_region" {
  type = "string"
  default = "ap-southeast-1"
}

variable "logging_level" {
  type = "string"
  default = "INFO"
}
