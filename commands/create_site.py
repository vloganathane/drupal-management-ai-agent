"""
Create Site Command - Creates new Drupal sites using DDEV or Lando
"""

import os
import subprocess
from typing import Dict, Any
from pathlib import Path

from commands.base_command import BaseCommand
from services.site_setup_service import SiteSetupService
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class CreateSiteCommand(BaseCommand):
    """Command to create new Drupal sites with DDEV or Lando"""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        self.config = Config()
        self.site_setup_service = SiteSetupService()
    
    def validate_params(self) -> bool:
        """Validate required parameters for site creation"""
        required_params = ['project_name']
        
        for param in required_params:
            if param not in self.params:
                self.result["message"] = f"Missing required parameter: {param}"
                return False
        
        # Validate project name format
        project_name = self.params['project_name']
        if not project_name or not isinstance(project_name, str):
            self.result["message"] = "Invalid project name"
            return False
        
        # Validate platform
        platform = self.params.get('platform', 'ddev')
        if platform not in ['ddev', 'lando']:
            self.result["message"] = f"Unsupported platform: {platform}. Use 'ddev' or 'lando'"
            return False
        
        return True
    
    def execute(self) -> Dict[str, Any]:
        """Execute site creation command"""
        self.log_execution(f"Creating site {self.params['project_name']}")
        
        if not self.validate_params():
            return self.result
        
        try:
            project_name = self.params['project_name']
            platform = self.params.get('platform', 'ddev')
            
            # Create site using the site setup service
            site_result = self.site_setup_service.create_site(
                project_name=project_name
            )
            
            if site_result['success']:
                self.result = {
                    "success": True,
                    "message": f"Successfully created Drupal site '{project_name}' using {platform}",
                    "data": {
                        "project_name": project_name,
                        "platform": platform,
                        "site_path": site_result.get('site_path'),
                        "next_steps": [
                            f"cd {site_result.get('site_path', project_name)}",
                            f"{platform} start" if platform == 'ddev' else f"{platform} start",
                            f"{platform} drush si --account-name=admin --account-pass=admin -y"
                        ]
                    }
                }
            else:
                self.result = {
                    "success": False,
                    "message": f"Failed to create site: {site_result.get('message', 'Unknown error')}",
                    "data": {"error_details": site_result}
                }
            
        except Exception as e:
            logger.error(f"Site creation failed: {str(e)}")
            self.result = {
                "success": False,
                "message": f"Site creation failed: {str(e)}",
                "data": {"error": str(e)}
            }
        
        return self.result
