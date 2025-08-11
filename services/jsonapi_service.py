"""
JSON:API Service for Drupal content operations
Handles creation, editing, and media uploads
"""

import requests
from typing import Dict, Any, Optional
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class JSONAPIService:
    """Handle Drupal JSON:API interactions for content operations"""
    
    def __init__(self):
        self.base_url = config.drupal_base_url.rstrip('/')
        self.session = requests.Session()
        self._authenticate()
    
    def _authenticate(self) -> bool:
        """Authenticate with Drupal"""
        try:
            auth_response = self.session.post(
                f"{self.base_url}/user/login?_format=json",
                json={
                    "name": config.drupal_username,
                    "pass": config.drupal_password
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if auth_response.status_code == 200:
                logger.info("Successfully authenticated with Drupal")
                return True
            else:
                logger.warning("Authentication failed: %s", auth_response.status_code)
                return False
                
        except requests.RequestException as e:
            logger.error("Authentication error: %s", str(e))
            return False
    
    def create_node(self, title: str, body: str, content_type: str = "article", 
                   tags: Optional[list] = None) -> Dict[str, Any]:
        """
        Create a new Drupal node
        
        Args:
            title: Node title
            body: Node body content
            content_type: Content type machine name
            tags: Optional list of taxonomy terms
            
        Returns:
            Result dictionary with success status and node data
        """
        try:
            node_data = {
                "data": {
                    "type": f"node--{content_type}",
                    "attributes": {
                        "title": title,
                        "body": {
                            "value": body,
                            "format": "full_html"
                        },
                        "status": True
                    }
                }
            }
            
            # Add taxonomy terms if provided
            if tags:
                node_data["data"]["relationships"] = {
                    "field_tags": {
                        "data": [{"type": "taxonomy_term--tags", "id": tag} for tag in tags]
                    }
                }
            
            response = self.session.post(
                f"{self.base_url}/jsonapi/node/{content_type}",
                json=node_data,
                headers={"Content-Type": "application/vnd.api+json"},
                timeout=30
            )
            
            if response.status_code == 201:
                node = response.json()["data"]
                return {
                    "success": True,
                    "node_id": node["attributes"]["drupal_internal__nid"],
                    "url": f"{self.base_url}/node/{node['attributes']['drupal_internal__nid']}",
                    "uuid": node["id"]
                }
            else:
                return {
                    "success": False, 
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    def update_node(self, node_id: int, updates: Dict[str, Any], 
                   content_type: str = "article") -> Dict[str, Any]:
        """
        Update an existing Drupal node
        
        Args:
            node_id: Node ID to update
            updates: Dictionary of fields to update
            content_type: Content type machine name
            
        Returns:
            Result dictionary with success status
        """
        try:
            # First get the node to verify it exists
            node_response = self.session.get(
                f"{self.base_url}/jsonapi/node/{content_type}/{node_id}",
                timeout=30
            )
            
            if node_response.status_code != 200:
                return {"success": False, "error": f"Node {node_id} not found"}
            
            node_data = {
                "data": {
                    "type": f"node--{content_type}",
                    "id": str(node_id),
                    "attributes": updates
                }
            }
            
            response = self.session.patch(
                f"{self.base_url}/jsonapi/node/{content_type}/{node_id}",
                json=node_data,
                headers={"Content-Type": "application/vnd.api+json"},
                timeout=30
            )
            
            return {
                "success": response.status_code == 200,
                "node_id": node_id,
                "url": f"{self.base_url}/node/{node_id}"
            }
            
        except requests.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    def delete_node(self, node_id: int, content_type: str = "article") -> Dict[str, Any]:
        """
        Delete a Drupal node
        
        Args:
            node_id: Node ID to delete
            content_type: Content type machine name
            
        Returns:
            Result dictionary with success status
        """
        try:
            response = self.session.delete(
                f"{self.base_url}/jsonapi/node/{content_type}/{node_id}",
                timeout=30
            )
            
            return {
                "success": response.status_code == 204,
                "node_id": node_id
            }
            
        except requests.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    def upload_media(self, file_path: str, alt_text: str = "", 
                    title: str = "") -> Dict[str, Any]:
        """
        Upload media file to Drupal
        
        Args:
            file_path: Path to file to upload
            alt_text: Alternative text for image
            title: Media title
            
        Returns:
            Result dictionary with success status and media data
        """
        try:
            import os
            
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            filename = os.path.basename(file_path)
            
            with open(file_path, 'rb') as f:
                files = {'files[field_media_image_0]': (filename, f, 'image/jpeg')}
                data = {
                    'alt': alt_text or filename,
                    'title': title or filename
                }
                
                response = self.session.post(
                    f"{self.base_url}/jsonapi/media/image",
                    files=files,
                    data=data,
                    timeout=60
                )
                
                if response.status_code == 201:
                    media = response.json()["data"]
                    return {
                        "success": True,
                        "media_id": media["attributes"]["drupal_internal__mid"],
                        "uuid": media["id"],
                        "filename": filename
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Upload failed: HTTP {response.status_code}"
                    }
                    
        except requests.RequestException as e:
            return {"success": False, "error": f"Upload failed: {str(e)}"}
