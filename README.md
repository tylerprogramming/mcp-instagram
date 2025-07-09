# Instagram MCP Server + CrewAI Integration

This project enables automated posting to Instagram (including carousels) using a local Model Context Protocol (MCP) server and a CrewAI agent. It is designed for advanced automation, leveraging the Instagram Graph API and CrewAI's agent/task orchestration.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
  - [Instagram MCP Server](#instagram-mcp-server)
  - [CrewAI Agent Orchestration](#crewai-agent-orchestration)
- [Setup Instructions](#setup-instructions)
  - [Environment Variables](#environment-variables)
  - [Dependencies](#dependencies)
- [Step-by-Step Usage](#step-by-step-usage)
- [Troubleshooting & Tips](#troubleshooting--tips)
- [References](#references)
- [Instagram API Setup: Step-by-Step](#instagram-api-setup-step-by-step)

---

## Overview

This system allows you to:
- Upload single images or carousels (multi-image posts) to Instagram via API.
- Use a CrewAI agent to automate the process, including caption formatting and media management.
- Integrate with other tools or workflows using the MCP protocol.

---

## How It Works

### Instagram MCP Server

The MCP server (`mcp_servers/instagram_server.py`) exposes Instagram API operations as tools, including:

- **refresh_instagram_access_token**: Refreshes your long-lived access token.
- **upload_image_without_caption**: Uploads an image and returns a media container ID (not published yet).
- **upload_image_with_caption**: Uploads an image with a caption and returns a media container ID.
- **upload_carousel_post**: Creates a carousel container from a list of media container IDs and a caption.
- **publish_media_container**: Publishes a previously uploaded media container (single image or carousel) to your Instagram feed.

**Workflow for Posting a Carousel:**
1. **Upload each image**: Each image is uploaded to Instagram, returning a media container ID.
2. **Create a carousel container**: The list of media container IDs is used to create a carousel post, along with a caption.
3. **Publish the carousel**: The carousel container is published to Instagram, making the post live.

**Workflow for Single Image:**
1. **Upload the image**: The image is uploaded (with or without a caption), returning a media container ID.
2. **Publish the image**: The media container is published to Instagram.

### CrewAI Agent Orchestration

The CrewAI agent (see `main.py`) automates the Instagram posting process:

- **Agent Setup**: The agent is initialized with access to the MCP server tools.
- **Task Description**: The agent receives a detailed task, including:
  - How to format the caption (Markdown-like, with line breaks).
  - The list of image URLs to use.
  - The order of operations for uploading and publishing.
  - Logic for handling carousels vs. single-image posts.
- **Execution**: The agent:
  1. Uploads all images and collects their media IDs.
  2. Depending on user input, creates a carousel or single image post.
  3. Publishes the post to Instagram.

---

## Setup Instructions

### Environment Variables

Create a `.env` file in your project root with the following variables:

```
INSTAGRAM_ACCESS_TOKEN=your_long_lived_access_token
INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id
HOST_URL=graph.facebook.com
LATEST_API_VERSION=v22.0
```

- **INSTAGRAM_ACCESS_TOKEN**: Obtain a long-lived access token via the [Instagram Graph API](https://developers.facebook.com/docs/instagram-basic-display-api/guides/long-lived-access-tokens).
- **INSTAGRAM_ACCOUNT_ID**: Your Instagram Business Account ID (see [Meta docs](https://developers.facebook.com/docs/instagram-api/getting-started)).
- **HOST_URL**: Usually `graph.facebook.com`.
- **LATEST_API_VERSION**: Use the latest supported version, e.g., `v22.0`.

### Dependencies

- Python 3.10+
- Required packages (install via pip):
  ```
  pip install crewai crewai_tools python-dotenv requests
  ```
- (Optional) Other dependencies as needed for your environment.

---

## Step-by-Step Usage

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or manually as above
   ```

3. **Set up your environment variables**:
   - Copy `.env.example` to `.env` and fill in your credentials.

4. **Start the MCP Instagram server**:
   ```bash
   python mcp_instagram/mcp_servers/instagram_server.py
   ```
   - This will start the server and expose Instagram API tools via MCP.

5. **Run the CrewAI Instagram agent**:
   ```bash
   python mcp_instagram/main.py
   ```
   - You will be prompted to enter the type of post (`carousel` or `single image publish`).
   - The agent will:
     - Format the caption using the latest YouTube transcription.
     - Upload images.
     - Create and publish the post as specified.

6. **Check the output**:
   - The script will print the result of the Instagram API call (success or error).

---

## Troubleshooting & Tips

- **Access Token Expiry**: If you get authentication errors, refresh your long-lived access token using the provided tool or via the Meta API.
- **Image URLs**: Ensure all image URLs are publicly accessible (no authentication required).
- **Account Type**: Only Instagram Business or Creator accounts linked to a Facebook Page can use the API.
- **API Limits**: Instagram enforces rate limits (e.g., 100 posts per 24 hours). Carousels count as a single post.
- **Error Handling**: Check the printed API responses for error messages and consult the [Meta error code reference](https://developers.facebook.com/docs/graph-api/using-graph-api/error-handling/).

---

## References

- [Meta Instagram Graph API Docs](https://developers.facebook.com/docs/instagram-api/)
- [Content Publishing Guide](https://developers.facebook.com/docs/instagram-platform/content-publishing/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Python Requests Library](https://docs.python-requests.org/en/latest/)
- [Model Context Protocol (MCP)](https://github.com/joaomdmoura/model-context-protocol)

---

## Instagram API Setup: Step-by-Step

Follow these steps to obtain the required credentials for Instagram API access. For more details, see the [Meta for Developers documentation](https://developers.facebook.com/).

1. **Create a Facebook App**
   - Go to the [Meta for Developers portal](https://developers.facebook.com/).
   - Log in and click **"My Apps"** > **"Create App"**.
   - Choose **"Business"** as the app type.
   - Fill in the required details (App Name, Contact Email, etc.).
   - Complete the app creation process.

2. **Configure Instagram Graph API**
   - In your app dashboard, click **"Add Product"** in the left sidebar.
   - Find **Instagram Graph API** and click **"Set Up"**.
   - Follow the prompts to add the product to your app.

3. **Set Up Instagram Business Account and Facebook Page**
   - **Instagram Account:**
     - Make sure your Instagram account is a **Business** or **Creator** account.
     - In the Instagram app:
       - Go to **Settings > Account > Switch to Professional Account**.
       - Choose **Business** or **Creator**.
   - **Link to Facebook Page:**
     - In Instagram:
       - Go to **Settings > Account > Linked Accounts > Facebook**.
       - Link your Instagram account to a Facebook Page you manage.

4. **Get Required Permissions**
   - In your app dashboard, go to **App Review > Permissions and Features**.
   - Request the following permissions:
     - `instagram_basic`
     - `instagram_content_publish`
     - `pages_read_engagement`
   - For production use, your app will need to go through App Review.

5. **Get a User Access Token**
   - Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
   - Select your app from the dropdown.
   - Click **"Get User Access Token"**.
   - Select the permissions you need (see above).
   - Click **"Generate Access Token"** and log in with your Facebook account.
   - Copy the **short-lived access token**.

6. **Exchange for a Long-Lived Access Token**
   - Use the following cURL command (replace placeholders with your values):
     ```bash
     curl -X GET "https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_ACCESS_TOKEN"
     ```
   - `YOUR_APP_ID` and `YOUR_APP_SECRET` are found in your app's **Settings > Basic**.
   - `SHORT_LIVED_ACCESS_TOKEN` is from the previous step.
   - The response will include a **long-lived access token**. Use this as your `INSTAGRAM_ACCESS_TOKEN`.

7. **Get Your Instagram Business Account ID**
   - Use the following cURL command (replace placeholders):
     ```bash
     curl -X GET "https://graph.facebook.com/v22.0/me/accounts?fields=instagram_business_account&access_token=LONG_LIVED_ACCESS_TOKEN"
     ```
   - The response will look like:
     ```json
     {
       "data": [
         {
           "instagram_business_account": {
             "id": "17841400000000000"
           },
           ...
         }
       ]
     }
     ```
   - The value of `"id"` is your **Instagram Business Account ID**. Use this as your `INSTAGRAM_ACCOUNT_ID`.

8. **Add to Your `.env` File**
   ```
   INSTAGRAM_ACCESS_TOKEN=your_long_lived_access_token
   INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id
   HOST_URL=graph.facebook.com
   LATEST_API_VERSION=v22.0
   ```

---


