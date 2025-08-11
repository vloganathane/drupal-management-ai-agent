"""
Drush Service for CLI operations
Handles cache clearing, cron, and other Drush commands
"""

import subprocess
from typing import Dict, Any, List, Optional
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class DrushService:
    """Handle Drush command execution"""
    
    def __init__(self, site_path: Optional[str] = None):
        self.drush_path = config.drush_path
        self.site_path = site_path or "."
    
    def execute_command(self, command: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute a Drush command
        
        Args:
            command: Drush command (without 'drush' prefix)
            args: Additional command arguments
            
        Returns:
            Command execution result
        """
        try:
            cmd_parts = [self.drush_path, command]
            if args:
                cmd_parts.extend(args)
            
            logger.info("Executing Drush command: %s", ' '.join(cmd_parts))
            
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                cwd=self.site_path,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "return_code": result.returncode,
                "command": ' '.join(cmd_parts)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out after 5 minutes",
                "command": ' '.join(cmd_parts)
            }
        except subprocess.SubprocessError as e:
            return {
                "success": False,
                "error": f"Subprocess error: {str(e)}",
                "command": ' '.join(cmd_parts)
            }
    
    def cache_rebuild(self) -> Dict[str, Any]:
        """Rebuild Drupal cache"""
        return self.execute_command("cache:rebuild")
    
    def cache_clear(self, bin_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Clear specific cache bin or all caches
        
        Args:
            bin_name: Specific cache bin to clear (optional)
            
        Returns:
            Command result
        """
        if bin_name:
            return self.execute_command("cache:clear", [bin_name])
        else:
            return self.execute_command("cache:clear")
    
    def run_cron(self) -> Dict[str, Any]:
        """Run Drupal cron"""
        return self.execute_command("cron:run")
    
    def update_database(self) -> Dict[str, Any]:
        """Run database updates"""
        return self.execute_command("updatedb", ["--yes"])
    
    def import_config(self) -> Dict[str, Any]:
        """Import configuration"""
        return self.execute_command("config:import", ["--yes"])
    
    def export_config(self) -> Dict[str, Any]:
        """Export configuration"""
        return self.execute_command("config:export", ["--yes"])
    
    def enable_module(self, module_name: str) -> Dict[str, Any]:
        """
        Enable a Drupal module
        
        Args:
            module_name: Module machine name
            
        Returns:
            Command result
        """
        return self.execute_command("pm:enable", [module_name, "--yes"])
    
    def disable_module(self, module_name: str) -> Dict[str, Any]:
        """
        Disable a Drupal module
        
        Args:
            module_name: Module machine name
            
        Returns:
            Command result
        """
        return self.execute_command("pm:disable", [module_name, "--yes"])
    
    def get_site_status(self) -> Dict[str, Any]:
        """Get Drupal site status"""
        return self.execute_command("status", ["--format=json"])
    
    def install_site(self, profile: str = "standard", site_name: str = "Drupal Site") -> Dict[str, Any]:
        """
        Install Drupal site
        
        Args:
            profile: Installation profile
            site_name: Site name
            
        Returns:
            Installation result
        """
        return self.execute_command("site:install", [
            profile,
            "--yes",
            f"--site-name={site_name}",
            f"--account-name={config.drupal_username}",
            f"--account-pass={config.drupal_password}"
        ])
    
    def generate_content(self, content_type: str, count: int = 10) -> Dict[str, Any]:
        """
        Generate dummy content using Devel Generate
        
        Args:
            content_type: Content type machine name
            count: Number of nodes to generate
            
        Returns:
            Generation result
        """
        return self.execute_command("devel:generate-content", [
            f"--bundles={content_type}",
            f"--num={count}",
            "--yes"
        ])
