# ☁️ How to Setup Google Cloud & Get API Keys

This guide explains how to obtain all the necessary credentials (`API Keys`, `Service Accounts`, `Config Strings`) to run the **Thesis AI Generator**.

---

## 1. Google Cloud Project Setup (The Foundation)

All services (Vertex AI, Cloud SQL, Storage) require a Google Cloud Project.

1.  Go to the **[Google Cloud Console](https://console.cloud.google.com/)**.
2.  Click the project dropdown (top left) and select **"New Project"**.
3.  Name it (e.g., `thesis-ai-gen`) and click **Create**.
4.  **Enable Billing**: Most AI services require an active billing account (even if they have free tiers).

---

## 2. Enable Required APIs

You must explicitly enable the services we are using.

1.  Go to **[APIs & Services > Library](https://console.cloud.google.com/apis/library)**.
2.  Search for and **Enable** the following APIs:
    *   **Vertex AI API** (For Gemini Models)
    *   **Cloud Document AI API** (For PDF/OCR processing)
    *   **Cloud Storage API** (For file hosting)
    *   **Cloud SQL Admin API** (For database connection)
    *   **Identity Toolkit API** (For Firebase Auth)

---

## 3. Get the Master Service Account Key (`GOOGLE_APPLICATION_CREDENTIALS`)

This single file allows your backend to talk to most GCP services (Vertex AI, Storage, Document AI).

1.  Go to **IAM & Admin > Service Accounts**.
2.  Click **+ Create Service Account**.
    *   **Name**: `thesis-backend-sa`
3.  **Grant Access (Roles)**:
    *   `Vertex AI User`
    *   `Storage Admin`
    *   `Document AI Editor`
    *   `Cloud SQL Client`
4.  Click **Done**.
5.  Click on the newly created email address (e.g., `thesis-backend-sa@...`).
6.  Go to the **Keys** tab > **Add Key** > **Create new key** > **JSON**.
7.  A file will download. **Rename it** to `service_account.json` and place it in your project root.
    *   **Update `.env`**: `GOOGLE_APPLICATION_CREDENTIALS=service_account.json`

---

## 4. Cloud SQL Setup (Database)

1.  Go to **[Cloud SQL](https://console.cloud.google.com/sql)**.
2.  Click **Create Instance** > **PostgreSQL**.
3.  Set a **Password** for the `postgres` user (Save this for `.env`).
4.  Once created, look at the **Overview** page for the **"Connection name"**.
    *   Format: `project-id:region:instance-name`
5.  **Update `.env`**:
    *   `CLOUD_SQL_CONNECTION_NAME=project-id:region:instance-name`
    *   `DB_PASS=your_password`

---


---

## 6. Gemini API Key (Alternative for Dev)

If you prefer using Google AI Studio instead of Vertex AI for development:

1.  Go to **[Google AI Studio](https://aistudio.google.com/)**.
2.  Click **Get API Key**.
3.  **Update `.env`**: `GOOGLE_API_KEY=your_key_here`

---

## ✅ Summary: Files You Should Have

| File / Value | Source | Purpose |
| :--- | :--- | :--- |
| `service_account.json` | GCP IAM | Access to Storage, DocAI, Vertex AI |

| `CLOUD_SQL_CONNECTION_NAME` | GCP Cloud SQL | Connecting to the database |
| `.env` | Created by you | Stores secrets and paths to the above files |

**⚠️ IMPORTANT:** Never commit these JSON files or your `.env` to GitHub. They are ignored by `.gitignore` by default.
