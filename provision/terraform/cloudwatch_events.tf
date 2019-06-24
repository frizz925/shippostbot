resource "aws_cloudwatch_event_rule" "shippostbot_scheduler" {
  name = "ShippostBotFacebookScheduler"
  description = "The default posting schedule"
  schedule_expression = "cron(0/30 * * * ? *)"

  tags = {
    App = "ShippostBot"
    Environment = "Production"
    Service = "CloudWatchEvent"
    Role = "Scheduler"
  }
}
