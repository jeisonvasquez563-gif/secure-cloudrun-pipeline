output "service_url" {
  description = "Public URL of the Cloud Run service."
  value       = google_cloud_run_v2_service.app.uri
}

output "artifact_registry_repository" {
  description = "Value for the AR_REPOSITORY repository variable in GitHub."
  value       = google_artifact_registry_repository.images.repository_id
}

output "wif_provider" {
  description = "Value for the WIF_PROVIDER repository variable in GitHub."
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "deployer_service_account" {
  description = "Value for the DEPLOYER_SA repository variable in GitHub."
  value       = google_service_account.deployer.email
}
