"""A simple Instagram MCP server that implements the Model Context Protocol.

This server provides Instagram operations as tools that can be discovered and used by MCP clients.
"""
import requests
import os

from typing import List, Optional
from mcp.server.fastmcp import FastMCP

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
HOST_URL = os.getenv("HOST_URL")
LATEST_API_VERSION = os.getenv("LATEST_API_VERSION")

mcp = FastMCP("Instagram MCP Server")

@mcp.tool(
    name="refresh_instagram_access_token",
    description="Refresh the long-lived Instagram access token.",
)
def refresh_instagram_access_token() -> None:
    """
    Refresh the long-lived Instagram access token.
    
    This tool requests a new long-lived access token for the Instagram account, extending its validity period.
    No parameters are required. Prints the response from the Instagram API.
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/refresh_access_token?grant_type=ig_refresh_token&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url)
    print(response.json())

@mcp.tool(
    name="upload_image_without_caption",
    description="Upload an image to Instagram (without caption) and return the media container ID.",
)
def upload_image_without_caption(image_url: str) -> dict:
    """
    Upload an image to Instagram (no caption).
    
    This tool uploads a single image to Instagram using only the image URL. It does not attach a caption and does not immediately publish the post.
    
    Args:
        image_url (str): The publicly accessible URL of the image to upload.
    
    Returns:
        dict: The JSON response from the Instagram API, including the media container ID if successful.
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}"
    }
    payload = {
        "image_url": image_url
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Upload Response:", response.json())
    return response.json()

@mcp.tool(
    name="upload_image_with_caption",
    description="Upload an image to Instagram with a caption and return the media container ID.",
)
def upload_image_with_caption(image_url: str, caption: str) -> Optional[str]:
    """
    Upload an image to Instagram with a caption.
    
    This tool uploads a single image to Instagram with a caption. It does not immediately publish the post, but returns the media container ID for later publishing.
    
    Args:
        image_url (str): The publicly accessible URL of the image to upload.
        caption (str): The caption to attach to the image.
    
    Returns:
        Optional[str]: The media container ID if successful, otherwise None.
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    media_id = response.json().get("id")
    print("Response:", response.json())
    print("Media ID:", media_id)
    return media_id

@mcp.tool(
    name="upload_carousel_post",
    description="Upload a carousel post (multiple images) to Instagram with a caption and return the media container ID.",
)
def upload_carousel_post(caption: str, children_ids: List[str]) -> dict:
    """
    Create an Instagram carousel (multi-image) post.
    
    This tool creates a carousel post (multiple images or videos) on Instagram. You must provide a caption and a list of previously uploaded media container IDs (children).
    
    Args:
        caption (str): The caption for the carousel post.
        children_ids (List[str]): List of media container IDs to include in the carousel.
    
    Returns:
        dict: The JSON response from the Instagram API, including the carousel container ID if successful.
    """
    url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "caption": caption,
        "media_type": "CAROUSEL",
        "children": children_ids,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    
    response = requests.post(url, headers=headers, json=payload)
    print("Carousel Upload Response:", response.json())
    return "payload: " + str(payload) + " response: " + str(response.json())

@mcp.tool(
    name="publish_media_container",
    description="Publish a previously uploaded Instagram media container.",
)
def publish_media_container(media_id: str) -> dict:
    """
    Publish a previously uploaded Instagram media container.
    
    This tool publishes a media container (image, video, or carousel) to the Instagram feed. The container must have been created previously using one of the upload tools.
    
    Args:
        media_id (str): The media container ID to publish.
    
    Returns:
        dict: The JSON response from the Instagram API, including the published post ID if successful.
    """
    publish_url = f"https://{HOST_URL}/{LATEST_API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_response = requests.post(
        publish_url,
        data={
            "creation_id": media_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
    )
    print("Publish Response:", publish_response.json())
    return publish_response.json()

if __name__ == "__main__":
    print("Starting Instagram MCP server...")
    mcp.run()