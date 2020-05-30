resource "aws_s3_bucket" "shippostbot_s3" {
  bucket = "${var.s3_bucket_name}"
  acl    = "private"

  tags = {
    App         = "ShippostBot"
    Environment = "Production"
    Service     = "S3"
    Access      = "PublicRead"
  }
}

resource "aws_iam_policy" "shippostbot_s3_access_policy" {
  name        = "ShippostBotS3FullAccess"
  path        = "/shippostbot/"
  description = "Policy to allow full access to ShippostBot buckets"
  policy      = "${data.aws_iam_policy_document.shippostbot_s3_access_policy.json}"
}

data "aws_iam_policy_document" "shippostbot_s3_access_policy" {
  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = ["${aws_s3_bucket.shippostbot_s3.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "shippostbot_s3_policy" {
  bucket = "${aws_s3_bucket.shippostbot_s3.id}"
  policy = "${data.aws_iam_policy_document.shippostbot_s3_policy.json}"
}

data "aws_iam_policy_document" "shippostbot_s3_policy" {
  statement {
    sid    = "AllowLambdaFunctions"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    principals {
      type        = "AWS"
      identifiers = ["${aws_iam_role.shippostbot_lambda_role.arn}"]
    }
    resources = [
      "${aws_s3_bucket.shippostbot_s3.arn}",
      "${aws_s3_bucket.shippostbot_s3.arn}/*",
    ]
  }

  statement {
    sid     = "AllowPublicRead"
    effect  = "Allow"
    actions = ["s3:GetObject"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    resources = ["${aws_s3_bucket.shippostbot_s3.arn}/*"]
  }
}
