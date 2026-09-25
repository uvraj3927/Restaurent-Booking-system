# ==============================================================================
# S3 BUCKET FOR FRONTEND STATIC WEBSITE
# ==============================================================================

# 1. Random suffix to make the bucket name globally unique
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# 2. Create S3 Bucket
resource "aws_s3_bucket" "frontend_bucket" {
  bucket        = "restaurant-booking-frontend-${random_id.bucket_suffix.hex}"
  force_destroy = true # Allows easy deletion of non-empty bucket via `terraform destroy`

  tags = {
    Name        = "restaurant-frontend"
    Environment = "Dev"
  }
}

# 3. Enable Static Website Hosting Configuration
resource "aws_s3_bucket_website_configuration" "frontend_website" {
  bucket = aws_s3_bucket.frontend_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

# 4. Disable "Block Public Access" so the website can be publicly viewed
resource "aws_s3_bucket_public_access_block" "public_access_block" {
  bucket = aws_s3_bucket.frontend_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 5. Attach Public Read Policy
resource "aws_s3_bucket_policy" "frontend_public_policy" {
  bucket = aws_s3_bucket.frontend_bucket.id

  # Ensure public access settings are removed before applying policy
  depends_on = [aws_s3_bucket_public_access_block.public_access_block]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend_bucket.arn}/*"
      }
    ]
  })
}

# 6. Output the Frontend Website URL
output "s3_website_url" {
  description = "URL of the S3 Static Website"
  value       = aws_s3_bucket_website_configuration.frontend_website.website_endpoint
}
