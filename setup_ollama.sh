#!/bin/bash
"""
Ollama Setup Script for Drupal AI Agent
This script helps set up Ollama with a small, efficient language model
"""

echo "🤖 Setting up Ollama for Drupal AI Agent..."
echo

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo "📦 Please install Ollama first:"
    echo "   • Visit: https://ollama.ai/"
    echo "   • Or run: curl -fsSL https://ollama.ai/install.sh | sh"
    echo
    exit 1
fi

echo "✅ Ollama is installed"

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🚀 Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Check if the service is now running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama service is running"
else
    echo "❌ Failed to start Ollama service"
    echo "💡 Try running 'ollama serve' manually"
    exit 1
fi

# Pull the recommended small model
echo "📥 Pulling llama3.2:1b (small, efficient model)..."
if ollama pull llama3.2:1b; then
    echo "✅ Model llama3.2:1b downloaded successfully"
else
    echo "⚠️  Failed to download llama3.2:1b, trying llama3.2:3b as fallback..."
    if ollama pull llama3.2:3b; then
        echo "✅ Model llama3.2:3b downloaded successfully"
        echo "💡 Update OLLAMA_MODEL=llama3.2:3b in your .env file"
    else
        echo "❌ Failed to download models. Check your internet connection."
        exit 1
    fi
fi

echo
echo "🎉 Ollama setup complete!"
echo "📝 The Drupal AI Agent is now configured to use local AI models"
echo "🔧 You can change the model by setting OLLAMA_MODEL in your .env file"
echo
echo "Available commands:"
echo "  • Test the setup: python main_modular.py execute 'create post about local AI'"
echo "  • List models: ollama list"
echo "  • Pull other models: ollama pull <model-name>"
echo
