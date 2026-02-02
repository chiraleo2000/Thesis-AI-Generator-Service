# 🔍 How to Obtain Missing IDs

You are nearly done! You just need two specific IDs from the Google Cloud Console.

## 1. Get `DOCUMENT_AI_PROCESSOR_ID`

This ID identifies the specific OCR processor (OCR parser) we will use.

1.  Go to the **[Document AI Console](https://console.cloud.google.com/ai/document-ai/processors)**.
2.  Click **+ CREATE PROCESSOR**.
3.  Scroll or search for **"Document OCR"** (Optical Character Recognition).
4.  Click **Create**.
    *   **Processor name**: `thesis-ocr` (or any name).
    *   **Region**: `US` (or EU).
5.  Click **Create**.
6.  Once created, you will see the **Processor Details** page.
7.  Copy the **Processor ID** (e.g., `53934d6c07...`).
8.  Update your `.env` file:
    ```bash
    DOCUMENT_AI_PROCESSOR_ID=53934d6c07...
    ```

## 2. Get `GOOGLE_SEARCH_CX` (Search Engine ID)

This ID allows the AI to search the web using a "Programmable Search Engine".

1.  Go to the **[Programmable Search Engine Control Panel](https://programmablesearchengine.google.com/controlpanel/all)**.
2.  Click **Add**.
3.  **Name**: `Thesis Search`.
4.  **What to search?**: Select **"Search the entire web"**.
5.  Click **Create**.
6.  You will be taken to the overview page. Look for **"Search engine ID"** (it looks like `a1b2c3d4e5...`).
    *   *Note*: This is the `CX` value.
7.  Update your `.env` file:
    ```bash
    GOOGLE_SEARCH_CX=a1b2c3d4e5...
    ```

## 3. Verify Deployment

After updating the `.env` (locally) or the Environment Variables (on Cloud Run), restart your service.
