resource "aws_lambda_function" "shippostbot_lambda" {
  function_name = "ShippostBot"
  role = "${aws_iam_role.shippostbot_lambda_role.arn}"
  handler = "lambda_function.lambda_handler"

  filename = "../artifacts/shippostbot.zip"
  source_code_hash = "${filebase64sha256("../artifacts/shippostbot.zip")}"

  runtime = "python3.10"
  memory_size = 128
  timeout = 300

  layers = [
    "${aws_lambda_layer_version.shippostbot_dependencies.arn}"
  ]

  environment {
    variables = {
      S3_BUCKET_NAME = "${var.s3_bucket_name}"
      S3_REGION = "${var.aws_region}"
      EVENT_FACEBOOK_ARN = "${aws_cloudwatch_event_rule.shippostbot_facebook_scheduler.arn}"
      FACEBOOK_ACCESS_TOKEN = "${var.facebook_access_token}"
      FACEBOOK_PUBLISH_STYLE = "${var.facebook_publish_style}"
      SELECTION_TYPE = "${var.selection_type}"
      LOGGING_LEVEL = "${var.logging_level}"
    }
  }

  tags = {
    App = "ShippostBot"
    Environment = "Production"
    Service = "Lambda"
  }
}

resource "aws_lambda_layer_version" "shippostbot_dependencies" {
  layer_name = "ShippostBotDependencies"
  compatible_runtimes = ["python3.10"]
  license_info = "GPL-3.0-or-later"

  filename = "../artifacts/shippostbot-deps.zip"
  source_code_hash = "${filebase64sha256("../artifacts/shippostbot-deps.zip")}"
}

resource "aws_lambda_permission" "shippostbot_lambda_exec" {
  statement_id = "ShippostBotExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.shippostbot_lambda.function_name}"
  principal = "events.amazonaws.com"
  source_arn = "${aws_cloudwatch_event_rule.shippostbot_facebook_scheduler.arn}"
}

resource "aws_cloudwatch_event_target" "shippostbot_lambda_event" {
  target_id = "ShippostBotExecutionEvent"
  rule = "${aws_cloudwatch_event_rule.shippostbot_facebook_scheduler.name}"
  arn = "${aws_lambda_function.shippostbot_lambda.arn}"
}

resource "aws_iam_role_policy_attachment" "shippostbot_lambda_log" {
  role = "${aws_iam_role.shippostbot_lambda_role.name}"
  policy_arn = "${aws_iam_policy.shippostbot_log_access_policy.arn}"
}

resource "aws_iam_role_policy_attachment" "shippostbot_lambda_s3" {
  role = "${aws_iam_role.shippostbot_lambda_role.name}"
  policy_arn = "${aws_iam_policy.shippostbot_s3_access_policy.arn}"
}

resource "aws_iam_role" "shippostbot_lambda_role" {
  name = "ShippostBot-lambda-role"
  path = "/shippostbot/"
  assume_role_policy = "${data.aws_iam_policy_document.shippostbot_lambda_role.json}"
}

data "aws_iam_policy_document" "shippostbot_lambda_role" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
