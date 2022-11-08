variable project_id {
  default = "XXX"
}

variable region {
  default = "us-central1"
}
variable private_key {
  default = <<EOH
-----BEGIN RSA PRIVATE KEY-----
XXXXXXXX
-----END RSA PRIVATE KEY-----
EOH
}
