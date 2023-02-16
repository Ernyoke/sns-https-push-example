resource "aws_dynamodb_table" "sns_subscrptions" {
  name           = "SNSSubs"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "SubscriptionARN"

  attribute {
    name = "SubscriptionARN"
    type = "S"
  }

#   attribute {
#     name = "TopicArn"
#     type = "S"
#   }

#   attribute {
#     name = "Status"
#     type = "S"
#   }

#   attribute {
#     name = "SubscribedTimeStamp"
#     type = "S"
#   }

#   attribute {
#     name = "UnsubscibedTimestamp"
#     type = "S"
#   }

  tags = {
    Name = "SNSSubs"
  }
}