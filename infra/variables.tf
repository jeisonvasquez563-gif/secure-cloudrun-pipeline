variable "project_id" {
  description = "Google Cloud project that hosts the service."
  type        = string
}

variable "region" {
  description = "Region for Cloud Run and Artifact Registry."
  type        = string
  default     = "us-central1"
}

variable "github_repository" {
  description = "GitHub repository allowed to deploy, in OWNER/REPO form."
  type        = string
}

variable "service_name" {
  description = "Cloud Run service name (also prefixes the service accounts)."
  type        = string
  default     = "secure-demo"
}

variable "allow_unauthenticated" {
  description = "Make the demo service publicly invokable. Set to false for private services."
  type        = bool
  default     = true
}
