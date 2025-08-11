"""
Output formatting utilities
"""

import json
from typing import Dict, Any
from enum import Enum

class OutputFormat(Enum):
    """Supported output formats"""
    JSON = "json"
    TEXT = "text"
    TABLE = "table"

class OutputFormatter:
    """Class for formatting output in different formats"""
    
    def format_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON"""
        return json.dumps(data, indent=2)
    
    def format_text(self, data: Dict[str, Any]) -> str:
        """Format data as human-readable text"""
        if data.get("success"):
            output = f"✅ {data['message']}\n"
            if data.get("data"):
                for key, value in data["data"].items():
                    output += f"   {key}: {value}\n"
        else:
            output = f"❌ {data['message']}\n"
        
        return output.strip()
    
    def format_table(self, data: Dict[str, Any]) -> str:
        """Format data as a simple table"""
        if not data.get("data"):
            return self.format_text(data)
        
        output = f"Status: {'SUCCESS' if data['success'] else 'FAILED'}\n"
        output += f"Message: {data['message']}\n"
        output += "-" * 50 + "\n"
        
        for key, value in data["data"].items():
            output += f"{key:<20}: {value}\n"
        
        return output

def format_output(data: Dict[str, Any], format_type: OutputFormat = OutputFormat.JSON) -> str:
    """
    Format output data according to specified format
    
    Args:
        data: Data to format
        format_type: Output format type
    
    Returns:
        Formatted string
    """
    formatter = OutputFormatter()
    
    if format_type == OutputFormat.JSON:
        return formatter.format_json(data)
    
    elif format_type == OutputFormat.TEXT:
        return formatter.format_text(data)
    
    elif format_type == OutputFormat.TABLE:
        return formatter.format_table(data)
    
    else:
        return str(data)

def _format_text(data: Dict[str, Any]) -> str:
    """Format data as human-readable text"""
    formatter = OutputFormatter()
    return formatter.format_text(data)

def _format_table(data: Dict[str, Any]) -> str:
    """Format data as a simple table"""
    formatter = OutputFormatter()
    return formatter.format_table(data)
