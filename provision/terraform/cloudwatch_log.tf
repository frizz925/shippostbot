resource "aws_cloudwatch_log_group" "shippostbot_log_group" {
  name = "/aws/lambda/ShippostBot"
  retention_in_days = 30

  tags = {
    App = "ShippostBot"
    Environment = "Production"
    Service = "CloudwatchLog"
    Role = "LogGroup"
  }
}

resource "aws_iam_policy" "shippostbot_log_access_policy" {
  name = "ShippostBotLogWrite"
  path = "/shippostbot/"
  description = "Policy to allow resources to put log events"
  policy = "${data.aws_iam_policy_document.shippostbot_log_access_policy.json}"
}

data "aws_iam_policy_document" "shippostbot_log_access_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["${aws_cloudwatch_log_group.shippostbot_log_group.arn}:*"]
  }
}
