# 🚀 Step-by-Step: Connect GitHub to Cloud Run

You have successfully added the `cloudbuild.yaml` and updated the code for Cloud Run. Now you must connect them in the Console.

## 1. Go to Google Cloud Console
1.  Navigate to **[Cloud Run](https://console.cloud.google.com/run)**.
2.  Click **+ CREATE SERVICE**.

## 2. Source Selection (Continuous Deployment)
*   **Select**: "Continuously deploy new revisions from a source repository".
*   Click **SET UP WITH CLOUD BUILD**.
*   **Repository Provider**: GitHub.
*   **Repository**: Select `Thesis-AI-Generator-Service`.
*   **Branch**: `^main$`
*   **Build Type**: Select **Use Dockerfile** (It will auto-detect the Dockerfile in the repo).
    *   *Note*: Since we also pushed a `cloudbuild.yaml`, you can also select "Cloud Build configuration file", but "Dockerfile" is often simpler for standard builds. Since you asked for "not the store image", this builds from source.
*   Click **SAVE**.

## 3. Configuration
*   **Service Name**: `thesis-ai-service`
*   **Region**: `us-central1`
*   **Authentication**: "Allow unauthenticated invocations" (Available public).

## 4. ⚠️ CRITICAL: Environment Variables
Since your `.env` file is **IGNORED** by Git (for security), Cloud Run does not know your API keys. You MUST add them manually here:

1.  Expand **Cainer, Networking, Security**.
2.  Click **VARIABLES & SECRETS** tab.
3.  Click **ADD VARIABLE** and add these from your local `.env`:
    *   `GCP_PROJECT_ID` = `thesis-ai-generator`
    *   `GCP_LOCATION` = `us-central1`
    *   `GOOGLE_APPLICATION_CREDENTIALS` = (See Note Below*)
    *   `GOOGLE_API_KEY` = `AQ.Ab8RN...`
    *   `GEMINI_MODEL_VERSION` = `gemini-3-flash-preview`
    *   `CLOUD_SQL_CONNECTION_NAME` = `thesis-ai-generator-db:us-central1:instance`
    *   `DB_USER` = `thesis-ai-generator-db`
    *   `DB_PASS` = `P@ssw0rd`
    *   `DB_NAME` = `thesis-ai-generator-data`

*Note on `GOOGLE_APPLICATION_CREDENTIALS`*: For Cloud Run, relying on the **Service Account** associated with the instance is better than passing a JSON file path. The default Compute Service Account usually has permissions if granted. You don't need to mount the JSON file if you grant the Cloud Run Service Account permissions to Vertex AI and SQL.*

## 5. Click CREATE
Cloud Build will start fetching your git repo, building the Docker image, and deploying it.
