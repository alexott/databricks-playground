resource "aws_iam_instance_profile" "vm_profile" {
  name = "${local.prefix}-profile"
  role = aws_iam_role.assume_role.name
  tags = var.tags
}

resource "aws_iam_role" "assume_role" {
  name               = "${local.prefix}-assume-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  tags               = var.tags
}

resource "aws_iam_policy" "get_web_identity_token" {
  name        = "allow-sts-get-web-identity-token"
  description = "Allow EC2 role to call sts:GetWebIdentityToken"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "sts:TagGetWebIdentityToken",
          "sts:GetWebIdentityToken",
          "sts:SetContext"
        ]
        Resource = "*"
        # Optional: restrict allowed audiences for tokens
        # Condition = {
        #   "ForAnyValue:StringEquals" = {
        #     "sts:IdentityTokenAudience" = [
        #       "https://api1.example.com",
        #       "https://api2.example.com"
        #     ]
        #   }
        # }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_get_web_identity" {
  role       = aws_iam_role.assume_role.name
  policy_arn = aws_iam_policy.get_web_identity_token.arn
}
