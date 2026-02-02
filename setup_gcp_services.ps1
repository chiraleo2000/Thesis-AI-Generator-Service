# Set Project
Write-Host "Setting GCP Project to thesis-ai-generator..."
gcloud config set project thesis-ai-generator

# Enable APIs
Write-Host "Enabling Required APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable documentai.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

Write-Host "APIs Enabled. You can now build and deploy."
