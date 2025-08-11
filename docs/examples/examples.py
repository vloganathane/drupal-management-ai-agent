#!/usr/bin/env python3
"""
GraphQL-Enhanced Query Examples for Drupal AI Agent

This file demonstrates the new GraphQL-enhanced query capabilities.
Run these examples to test the natural language parsing for data queries.
"""

from main import NLParser, CommandFactory

def demonstrate_query_capabilities():
    """Demonstrate all GraphQL-enhanced query capabilities"""
    
    parser = NLParser()
    
    print("🔍 GraphQL-Enhanced Query Examples")
    print("=" * 50)
    
    # Example queries
    examples = [
        # Node queries
        "Show me the titles of the latest 10 blog posts",
        "Get the latest 5 articles", 
        "Find posts about AI",
        "Fetch article bodies containing the word Drupal",
        "Query nodes of type page",
        
        # User queries  
        "Get all users with role 'editor'",
        "Show users with role admin",
        "List all authors",
        
        # Search queries
        "Find articles about machine learning",
        "Search for content about headless CMS",
    ]
    
    for example in examples:
        print(f"\n📝 Command: '{example}'")
        try:
            intent, params = parser.parse(example)
            print(f"   🎯 Intent: {intent}")
            print(f"   📋 Parameters: {params}")
            
            # Create command instance
            command = CommandFactory.create_command(intent, params)
            if command:
                print(f"   ✅ Command class: {command.__class__.__name__}")
            else:
                print(f"   ❌ No command class found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("💡 Usage Tips:")
    print("1. Use specific numbers for limits: 'latest 10 posts'")
    print("2. Put roles in quotes: 'role editor' or 'role \"content manager\"'")
    print("3. Search terms are automatically extracted from natural language")
    print("4. Content types are mapped: 'blog posts' → 'article', 'pages' → 'page'")

def demonstrate_graphql_queries():
    """Demonstrate direct GraphQL query examples"""
    
    print("\n🧬 Direct GraphQL Query Examples")
    print("=" * 50)
    
    # Example GraphQL queries that could be executed
    graphql_examples = [
        {
            "description": "Get latest 5 published articles with titles and authors",
            "query": """
            query {
              nodeQuery(filter: {
                conditions: [
                  {field: "type", value: "article"},
                  {field: "status", value: "1"}
                ]
              }, sort: [{field: "created", direction: DESC}], limit: 5) {
                entities {
                  ... on NodeArticle {
                    title
                    created
                    author: uid {
                      entity {
                        name
                      }
                    }
                  }
                }
              }
            }
            """
        },
        {
            "description": "Get users with editor role",
            "query": """
            query {
              userQuery(filter: {
                conditions: [
                  {field: "roles", value: "editor"}
                ]
              }) {
                entities {
                  name
                  mail
                  created
                }
              }
            }
            """
        },
        {
            "description": "Search articles containing 'Drupal'",
            "query": """
            query {
              nodeQuery(filter: {
                conditions: [
                  {field: "type", value: "article"},
                  {field: "title", value: "Drupal", operator: CONTAINS}
                ]
              }) {
                entities {
                  ... on NodeArticle {
                    title
                    body {
                      value
                    }
                  }
                }
              }
            }
            """
        }
    ]
    
    for i, example in enumerate(graphql_examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   Query: {example['query'].strip()}")

if __name__ == "__main__":
    demonstrate_query_capabilities()
    demonstrate_graphql_queries()
