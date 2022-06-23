output "token_value" {
  value     = databricks_token.pat.token_value
  sensitive = true
}