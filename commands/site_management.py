"""
Site Management Command - Start, stop, restart, and check status of Drupal sites
"""

import subprocess
from typing import Dict, Any
from commands.base_command import BaseCommand
from services.site_setup_service import SiteSetupService
from utils.logger import get_logger

logger = get_logger(__name__)

class StartSiteCommand(BaseCommand):
    """Command to start a Drupal site"""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        self.site_setup_service = SiteSetupService()
    
    def validate_params(self) -> bool:
        """Validate required parameters"""
        if 'project_name' not in self.params:
            self.result["message"] = "Missing required parameter: project_name"
            return False
        return True
    
    def execute(self) -> Dict[str, Any]:
        """Execute start site command"""
        self.log_execution(f"Starting site {self.params['project_name']}")
        
        if not self.validate_params():
            return self.result
        
        try:
            result = self.site_setup_service.start_site(
                project_name=self.params['project_name']
            )
            self.result = result
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            logger.error("Failed to start site: %s", str(e))
            self.result = {
                "success": False,
                "message": f"Failed to start site: {str(e)}",
                "data": {"error": str(e)}
            }
        
        return self.result


class StopSiteCommand(BaseCommand):
    """Command to stop a Drupal site"""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        self.site_setup_service = SiteSetupService()
    
    def validate_params(self) -> bool:
        """Validate required parameters"""
        if 'project_name' not in self.params:
            self.result["message"] = "Missing required parameter: project_name"
            return False
        return True
    
    def execute(self) -> Dict[str, Any]:
        """Execute stop site command"""
        self.log_execution(f"Stopping site {self.params['project_name']}")
        
        if not self.validate_params():
            return self.result
        
        try:
            result = self.site_setup_service.stop_site(
                project_name=self.params['project_name']
            )
            self.result = result
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            logger.error("Failed to stop site: %s", str(e))
            self.result = {
                "success": False,
                "message": f"Failed to stop site: {str(e)}",
                "data": {"error": str(e)}
            }
        
        return self.result


class RestartSiteCommand(BaseCommand):
    """Command to restart a Drupal site"""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        self.site_setup_service = SiteSetupService()
    
    def validate_params(self) -> bool:
        """Validate required parameters"""
        if 'project_name' not in self.params:
            self.result["message"] = "Missing required parameter: project_name"
            return False
        return True
    
    def execute(self) -> Dict[str, Any]:
        """Execute restart site command"""
        self.log_execution(f"Restarting site {self.params['project_name']}")
        
        if not self.validate_params():
            return self.result
        
        try:
            result = self.site_setup_service.restart_site(
                project_name=self.params['project_name']
            )
            self.result = result
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            logger.error("Failed to restart site: %s", str(e))
            self.result = {
                "success": False,
                "message": f"Failed to restart site: {str(e)}",
                "data": {"error": str(e)}
            }
        
        return self.result


class StatusSiteCommand(BaseCommand):
    """Command to check status of a Drupal site"""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        self.site_setup_service = SiteSetupService()
    
    def validate_params(self) -> bool:
        """Validate required parameters"""
        if 'project_name' not in self.params:
            self.result["message"] = "Missing required parameter: project_name"
            return False
        return True
    
    def execute(self) -> Dict[str, Any]:
        """Execute status site command"""
        self.log_execution(f"Checking status of site {self.params['project_name']}")
        
        if not self.validate_params():
            return self.result
        
        try:
            result = self.site_setup_service.status_site(
                project_name=self.params['project_name']
            )
            self.result = result
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            logger.error("Failed to get site status: %s", str(e))
            self.result = {
                "success": False,
                "message": f"Failed to get site status: {str(e)}",
                "data": {"error": str(e)}
            }
        
        return self.result
