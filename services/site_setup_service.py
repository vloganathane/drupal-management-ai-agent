"""
Site Setup Service for DDEV and Lando automation
Handles local Drupal site creation and configuration
"""

import subprocess
import os
from typing import Dict, Any, Optional
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class SiteSetupService:
    """Handle local Drupal site setup with DDEV or Lando"""

    def __init__(self, platform: str = "ddev"):
        self.platform = platform.lower()
        self.ddev_path = self._find_executable(config.ddev_path, "ddev")
        self.lando_path = self._find_executable(config.lando_path, "lando")

    @staticmethod
    def _find_executable(config_path, exe_name):
        import shutil
        exe_path = shutil.which(config_path) or shutil.which(exe_name)
        return exe_path

    def create_site(self, project_name: str, directory: Optional[str] = None, domain: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Drupal site using the configured platform"""
        site_dir = directory or config.default_site_directory
        project_path = os.path.join(site_dir, project_name)
        
        # Ensure the site directory exists
        try:
            if not os.path.exists(site_dir):
                os.makedirs(site_dir, exist_ok=True)
                logger.info(f"Created site directory: {site_dir}")
        except Exception as e:
            logger.error(f"Failed to create site directory: {e}")
            return {"success": False, "error": f"Failed to create site directory: {e}"}

        if os.path.exists(project_path):
            return {"success": False, "error": f"Site directory already exists: {project_path}"}

        # Check if DDEV or Lando is installed
        if self.platform == "ddev" and not self.ddev_path:
            return {
                "success": False,
                "error": "DDEV is not installed.",
                "instructions": (
                    "DDEV is required to create a Drupal site.\n"
                    "Install DDEV: https://ddev.com/get-started/\n"
                    "On macOS: brew install drud/ddev/ddev\n"
                    "On Linux: curl -LO https://raw.githubusercontent.com/ddev/ddev/master/scripts/install_ddev.sh && bash install_ddev.sh\n"
                    "On Windows: https://ddev.com/get-started/#windows"
                )
            }
        if self.platform == "lando" and not self.lando_path:
            return {
                "success": False,
                "error": "Lando is not installed.",
                "instructions": (
                    "Lando is required to create a Drupal site.\n"
                    "Install Lando: https://docs.lando.dev/basics/installation.html\n"
                    "On macOS: brew install lando\n"
                    "On Linux: curl -fsSL https://lando.dev/install.sh | bash\n"
                    "On Windows: https://docs.lando.dev/basics/installation.html#windows"
                )
            }

        try:
            if self.platform == "ddev":
                return self._create_ddev_site(project_name, project_path)
            elif self.platform == "lando":
                return self._create_lando_site(project_name, project_path)
            else:
                return {"success": False, "error": f"Unsupported platform: {self.platform}"}
        except Exception as e:
            logger.error(f"Site creation failed: {e}")
            return {"success": False, "error": str(e)}

    def _create_ddev_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Create Drupal site using DDEV in the correct directory"""
        try:
            logger.info(f"Creating DDEV site: {project_name} in {project_path}")
            
            # Create project directory
            os.makedirs(project_path, exist_ok=True)
            
            # Create Drupal project with Composer in project_path
            result = subprocess.run([
                "composer", "create-project", "drupal/recommended-project", ".",
                "--no-interaction", "--prefer-dist"
            ], capture_output=True, text=True, timeout=600, check=False, cwd=project_path)
            if result.returncode != 0:
                return {"success": False, "error": f"Composer failed: {result.stderr}"}

            # Configure DDEV in project_path
            ddev_config_cmd = [
                self.ddev_path, "config",
                f"--project-type={config.default_drupal_version}",
                f"--project-name={project_name}",
                "--docroot=web",
                "--create-docroot"
            ]
            result = subprocess.run(ddev_config_cmd, capture_output=True, text=True, timeout=60, check=False, cwd=project_path)
            if result.returncode != 0:
                return {"success": False, "error": f"DDEV config failed: {result.stderr}"}

            # Start DDEV in project_path
            result = subprocess.run([self.ddev_path, "start"], capture_output=True, text=True, timeout=180, check=False, cwd=project_path)
            if result.returncode != 0:
                return {"success": False, "error": f"DDEV start failed: {result.stderr}"}

            # Install Drupal in project_path
            result = subprocess.run([
                self.ddev_path, "drush", "site:install", "standard",
                "--yes",
                f"--site-name={project_name}",
                f"--account-name={config.drupal_username}",
                f"--account-pass={config.drupal_password}"
            ], capture_output=True, text=True, timeout=300, check=False, cwd=project_path)
            if result.returncode != 0:
                logger.warning(f"Drupal installation had issues: {result.stderr}")
                
            site_url = f"https://{project_name}.ddev.site"
            return {
                "success": True,
                "message": f"DDEV site '{project_name}' created successfully",
                "data": {
                    "project_name": project_name,
                    "url": site_url,
                    "platform": "ddev",
                    "directory": project_path,
                    "admin_user": config.drupal_username,
                    "admin_pass": config.drupal_password
                }
            }
        except Exception as e:
            logger.error(f"DDEV site creation failed: {e}")
            return {"success": False, "error": str(e)}

    def _create_lando_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Create Drupal site using Lando in the correct directory"""
        try:
            logger.info(f"Creating Lando site: {project_name} in {project_path}")
            
            # Create project directory
            os.makedirs(project_path, exist_ok=True)
            
            # Create Drupal project with Composer in project_path
            result = subprocess.run([
                "composer", "create-project", "drupal/recommended-project", ".",
                "--no-interaction", "--prefer-dist"
            ], capture_output=True, text=True, timeout=600, check=False, cwd=project_path)
            if result.returncode != 0:
                return {"success": False, "error": f"Composer failed: {result.stderr}"}

            # Create Lando configuration
            site_domain = f"{project_name}.lndo.site"
            lando_config = f"""name: {project_name}
recipe: drupal10
config:
  webroot: web
  database: mariadb:10.6
  php: '8.1'
proxy:
  appserver:
    - {site_domain}
services:
  appserver:
    build_as_root:
      - apt-get update -y && apt-get install -y vim
tooling:
  drush:
    service: appserver
    cmd: /app/vendor/bin/drush
"""
            with open(os.path.join(project_path, ".lando.yml"), "w") as f:
                f.write(lando_config)

            # Start Lando in project_path
            result = subprocess.run([self.lando_path, "start"], capture_output=True, text=True, timeout=300, check=False, cwd=project_path)
            if result.returncode != 0:
                return {"success": False, "error": f"Lando start failed: {result.stderr}"}

            # Install Drupal in project_path
            result = subprocess.run([
                self.lando_path, "drush", "site:install", "standard",
                "--yes",
                f"--site-name={project_name}",
                f"--account-name={config.drupal_username}",
                f"--account-pass={config.drupal_password}"
            ], capture_output=True, text=True, timeout=300, check=False, cwd=project_path)
            if result.returncode != 0:
                logger.warning(f"Drupal installation had issues: {result.stderr}")
                
            return {
                "success": True,
                "message": f"Lando site '{project_name}' created successfully",
                "data": {
                    "project_name": project_name,
                    "url": f"https://{site_domain}",
                    "platform": "lando",
                    "directory": project_path,
                    "admin_user": config.drupal_username,
                    "admin_pass": config.drupal_password
                }
            }
        except Exception as e:
            logger.error(f"Lando site creation failed: {e}")
            return {"success": False, "error": str(e)}

    def start_site(self, project_name: str, directory: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Start a Drupal site using DDEV or Lando"""
        site_dir = directory or config.default_site_directory
        project_path = os.path.join(site_dir, project_name)
        
        if not os.path.exists(project_path):
            return {"success": False, "error": f"Site directory not found: {project_path}"}
        
        # Auto-detect platform if not specified
        detected_platform = platform or self._detect_platform(project_path)
        
        if detected_platform == "ddev":
            return self._start_ddev_site(project_name, project_path)
        elif detected_platform == "lando":
            return self._start_lando_site(project_name, project_path)
        else:
            return {"success": False, "error": f"No DDEV or Lando configuration found in {project_path}"}

    def stop_site(self, project_name: str, directory: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Stop a Drupal site using DDEV or Lando"""
        site_dir = directory or config.default_site_directory
        project_path = os.path.join(site_dir, project_name)
        
        if not os.path.exists(project_path):
            return {"success": False, "error": f"Site directory not found: {project_path}"}
        
        # Auto-detect platform if not specified
        detected_platform = platform or self._detect_platform(project_path)
        
        if detected_platform == "ddev":
            return self._stop_ddev_site(project_name, project_path)
        elif detected_platform == "lando":
            return self._stop_lando_site(project_name, project_path)
        else:
            return {"success": False, "error": f"No DDEV or Lando configuration found in {project_path}"}

    def restart_site(self, project_name: str, directory: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Restart a Drupal site using DDEV or Lando"""
        site_dir = directory or config.default_site_directory
        project_path = os.path.join(site_dir, project_name)
        
        if not os.path.exists(project_path):
            return {"success": False, "error": f"Site directory not found: {project_path}"}
        
        # Auto-detect platform if not specified
        detected_platform = platform or self._detect_platform(project_path)
        
        if detected_platform == "ddev":
            return self._restart_ddev_site(project_name, project_path)
        elif detected_platform == "lando":
            return self._restart_lando_site(project_name, project_path)
        else:
            return {"success": False, "error": f"No DDEV or Lando configuration found in {project_path}"}

    def status_site(self, project_name: str, directory: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get status of a Drupal site using DDEV or Lando"""
        site_dir = directory or config.default_site_directory
        project_path = os.path.join(site_dir, project_name)
        
        if not os.path.exists(project_path):
            return {"success": False, "error": f"Site directory not found: {project_path}"}
        
        # Auto-detect platform if not specified
        detected_platform = platform or self._detect_platform(project_path)
        
        if detected_platform == "ddev":
            return self._status_ddev_site(project_name, project_path)
        elif detected_platform == "lando":
            return self._status_lando_site(project_name, project_path)
        else:
            return {"success": False, "error": f"No DDEV or Lando configuration found in {project_path}"}

    def _detect_platform(self, project_path: str) -> Optional[str]:
        """Auto-detect the platform (DDEV or Lando) used for the site"""
        ddev_config = os.path.join(project_path, ".ddev", "config.yaml")
        lando_config = os.path.join(project_path, ".lando.yml")
        
        if os.path.exists(ddev_config):
            return "ddev"
        elif os.path.exists(lando_config):
            return "lando"
        return None

    def _start_ddev_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Start DDEV site"""
        try:
            logger.info(f"Starting DDEV site: {project_name}")
            result = subprocess.run([self.ddev_path, "start"], capture_output=True, text=True, timeout=300, cwd=project_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"DDEV site '{project_name}' started successfully",
                    "data": {
                        "project_name": project_name,
                        "platform": "ddev",
                        "status": "running",
                        "directory": project_path,
                        "output": result.stdout
                    }
                }
            else:
                return {"success": False, "error": f"DDEV start failed: {result.stderr}"}
        except Exception as e:
            logger.error(f"Failed to start DDEV site: {e}")
            return {"success": False, "error": str(e)}

    def _stop_ddev_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Stop DDEV site"""
        try:
            logger.info(f"Stopping DDEV site: {project_name}")
            result = subprocess.run([self.ddev_path, "stop"], capture_output=True, text=True, timeout=120, cwd=project_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"DDEV site '{project_name}' stopped successfully",
                    "data": {
                        "project_name": project_name,
                        "platform": "ddev",
                        "status": "stopped",
                        "directory": project_path
                    }
                }
            else:
                return {"success": False, "error": f"DDEV stop failed: {result.stderr}"}
        except Exception as e:
            logger.error(f"Failed to stop DDEV site: {e}")
            return {"success": False, "error": str(e)}

    def _restart_ddev_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Restart DDEV site"""
        try:
            logger.info(f"Restarting DDEV site: {project_name}")
            result = subprocess.run([self.ddev_path, "restart"], capture_output=True, text=True, timeout=300, cwd=project_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"DDEV site '{project_name}' restarted successfully",
                    "data": {
                        "project_name": project_name,
                        "platform": "ddev",
                        "status": "running",
                        "directory": project_path
                    }
                }
            else:
                return {"success": False, "error": f"DDEV restart failed: {result.stderr}"}
        except Exception as e:
            logger.error(f"Failed to restart DDEV site: {e}")
            return {"success": False, "error": str(e)}

    def _status_ddev_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Get DDEV site status"""
        try:
            logger.info(f"Getting DDEV site status: {project_name}")
            result = subprocess.run([self.ddev_path, "status"], capture_output=True, text=True, timeout=60, cwd=project_path)
            
            return {
                "success": True,
                "message": f"DDEV site '{project_name}' status retrieved",
                "data": {
                    "project_name": project_name,
                    "platform": "ddev",
                    "directory": project_path,
                    "status_output": result.stdout,
                    "status_code": result.returncode
                }
            }
        except Exception as e:
            logger.error(f"Failed to get DDEV site status: {e}")
            return {"success": False, "error": str(e)}

    def _start_lando_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Start Lando site"""
        try:
            logger.info(f"Starting Lando site: {project_name}")
            result = subprocess.run([self.lando_path, "start"], capture_output=True, text=True, timeout=300, cwd=project_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Lando site '{project_name}' started successfully",
                    "data": {
                        "project_name": project_name,
                        "platform": "lando",
                        "status": "running",
                        "directory": project_path,
                        "output": result.stdout
                    }
                }
            else:
                return {"success": False, "error": f"Lando start failed: {result.stderr}"}
        except Exception as e:
            logger.error(f"Failed to start Lando site: {e}")
            return {"success": False, "error": str(e)}

    def _stop_lando_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Stop Lando site"""
        try:
            logger.info(f"Stopping Lando site: {project_name}")
            result = subprocess.run([self.lando_path, "stop"], capture_output=True, text=True, timeout=120, cwd=project_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Lando site '{project_name}' stopped successfully",
                    "data": {
                        "project_name": project_name,
                        "platform": "lando",
                        "status": "stopped",
                        "directory": project_path
                    }
                }
            else:
                return {"success": False, "error": f"Lando stop failed: {result.stderr}"}
        except Exception as e:
            logger.error(f"Failed to stop Lando site: {e}")
            return {"success": False, "error": str(e)}

    def _restart_lando_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Restart Lando site"""
        try:
            logger.info(f"Restarting Lando site: {project_name}")
            result = subprocess.run([self.lando_path, "restart"], capture_output=True, text=True, timeout=300, cwd=project_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Lando site '{project_name}' restarted successfully",
                    "data": {
                        "project_name": project_name,
                        "platform": "lando",
                        "status": "running",
                        "directory": project_path
                    }
                }
            else:
                return {"success": False, "error": f"Lando restart failed: {result.stderr}"}
        except Exception as e:
            logger.error(f"Failed to restart Lando site: {e}")
            return {"success": False, "error": str(e)}

    def _status_lando_site(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Get Lando site status"""
        try:
            logger.info(f"Getting Lando site status: {project_name}")
            result = subprocess.run([self.lando_path, "info"], capture_output=True, text=True, timeout=60, cwd=project_path)
            
            return {
                "success": True,
                "message": f"Lando site '{project_name}' status retrieved",
                "data": {
                    "project_name": project_name,
                    "platform": "lando",
                    "directory": project_path,
                    "status_output": result.stdout,
                    "status_code": result.returncode
                }
            }
        except Exception as e:
            logger.error(f"Failed to get Lando site status: {e}")
            return {"success": False, "error": str(e)}
