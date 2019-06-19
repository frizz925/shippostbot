variable "facebook_access_token" {
  type = "string"
}

variable "facebook_page_id" {
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
