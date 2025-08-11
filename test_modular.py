#!/usr/bin/env python3
"""
Test script for the modular Drupal AI Agent
Run this to validate the new architecture
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("🧪 Testing module imports...")
    
    try:
        # Core configuration
        from config import config
        print("✅ config module imported")
        
        # Utilities
        from utils.logger import setup_logging, get_logger
        from utils.output_formatter import format_output, OutputFormat
        print("✅ utils modules imported")
        
        # Services
        from services.ai_service import AIService
        from services.drush_service import DrushService
        from services.jsonapi_service import JSONAPIService
        from services.graphql_service import GraphQLService
        from services.site_setup_service import SiteSetupService
        print("✅ services modules imported")
        
        # Parsers
        from parsers.intent_parser import IntentParser
        from parsers.parameter_extractor import ParameterExtractor
        print("✅ parser modules imported")
        
        # Commands
        from commands.base_command import BaseCommand
        from commands.create_post import CreatePostCommand
        print("✅ command modules imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_parser():
    """Test the intent parser functionality"""
    print("\n🔍 Testing intent parser...")
    
    try:
        from parsers.intent_parser import IntentParser
        parser = IntentParser()
        
        test_commands = [
            "create post about AI and Drupal",
            "clear cache",
            "show latest 10 posts",
            "create site named test-site",
            "upload image file.jpg",
            "get users with role editor"
        ]
        
        for cmd in test_commands:
            intent, params = parser.parse(cmd)
            print(f"  '{cmd}' → {intent} (params: {len(params)} items)")
        
        return True
        
    except Exception as e:
        print(f"❌ Parser test error: {e}")
        return False

def test_command_creation():
    """Test command creation and validation"""
    print("\n⚙️  Testing command creation...")
    
    try:
        from commands.create_post import CreatePostCommand
        
        # Test with valid parameters
        params = {
            "title": "Test Post",
            "content_type": "article",
            "ai_provider": "openai"
        }
        
        command = CreatePostCommand(params)
        is_valid = command.validate_params()
        
        print(f"  CreatePostCommand validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Command creation test error: {e}")
        return False

def test_output_formatting():
    """Test output formatting functionality"""
    print("\n📋 Testing output formatting...")
    
    try:
        from utils.output_formatter import format_output, OutputFormat
        
        test_data = {
            "success": True,
            "message": "Test successful",
            "data": {
                "post_id": 123,
                "title": "Test Post",
                "url": "/node/123"
            }
        }
        
        # Test JSON format
        json_output = format_output(test_data, OutputFormat.JSON)
        print(f"  JSON format: {'✅ PASS' if '"success": true' in json_output else '❌ FAIL'}")
        
        # Test text format  
        text_output = format_output(test_data, OutputFormat.TEXT)
        print(f"  Text format: {'✅ PASS' if 'Test successful' in text_output else '❌ FAIL'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Output formatting test error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import config
        
        print(f"  Drupal URL: {config.drupal_base_url}")
        print(f"  AI Provider: {config.default_ai_provider}")
        print(f"  GraphQL endpoint: {config.graphql_endpoint}")
        
        has_required = bool(config.drupal_base_url and config.default_ai_provider)
        print(f"  Required config present: {'✅ PASS' if has_required else '❌ FAIL'}")
        
        return has_required
        
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Drupal AI Agent - Modular Architecture Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_configuration,
        test_parser,
        test_command_creation,
        test_output_formatting
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The modular architecture is working correctly.")
        print("\n🎯 Next steps:")
        print("1. Configure your .env file with Drupal credentials")
        print("2. Add AI provider API keys")
        print("3. Test with: python main.py execute 'create post about testing'")
        print("4. Run setup: python main.py setup")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
