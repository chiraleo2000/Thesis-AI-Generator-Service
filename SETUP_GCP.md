# ☁️ Deployment & Setup Guide for `thesis-ai-generator`

## 1. Google Cloud Project
**Project ID**: `thesis-ai-generator`
**Region**: `us-central1`

Ensure you have selected this project in your console or CLI:
```powershell
gcloud config set project thesis-ai-generator
```

## 2. Automated Service Setup
We have provided a script `setup_gcp_services.ps1` to enable all required APIs (Vertex AI, Document AI, Storage, SQL, Cloud Run).

Run it in your terminal:
```powershell
./setup_gcp_services.ps1
```

## 3. Configuration Values
Your `.env` has been configured with match the production environment:

*   **SQL Connection**: `thesis-ai-generator-db:us-central1:instance`
*   **Database**: `thesis-ai-generator-data`
*   **API Key**: (Configured)

## 4. Deploy to Cloud Run
To deploy the application as a scalable container:

```powershell
gcloud run deploy thesis-ai-service `
    --source . `
    --region us-central1 `
    --allow-unauthenticated `
    --env-vars-file .env
```
