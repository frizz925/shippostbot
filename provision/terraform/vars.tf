variable "facebook_access_token" {
  type = "string"
}

variable "facebook_publish_style" {
  type = "string"
  default = "POST_AND_COMMENT"
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

variable "selection_type" {
  type = "string"
  default = "FROM_CHARACTER_TO_MEDIA"
}
