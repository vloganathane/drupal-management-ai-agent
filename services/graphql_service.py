"""
GraphQL Service for Drupal content queries
Handles selective field retrieval and complex queries
"""

import requests
from typing import Dict, Any, List, Optional
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class GraphQLService:
    """Handle Drupal GraphQL interactions for content queries"""
    
    def __init__(self):
        self.base_url = config.drupal_base_url.rstrip('/')
        self.session = requests.Session()
        self._authenticate()
    
    def _authenticate(self) -> bool:
        """Authenticate with Drupal for GraphQL access"""
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
                logger.info("GraphQL authentication successful")
                return True
            else:
                logger.warning("GraphQL authentication failed: %s", auth_response.status_code)
                return False
                
        except requests.RequestException as e:
            logger.error("GraphQL authentication error: %s", str(e))
            return False
    
    def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Optional query variables
            
        Returns:
            Query result dictionary
        """
        try:
            payload = {
                "query": query,
                "variables": variables or {}
            }
            
            response = self.session.post(
                f"{self.base_url}/graphql",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False, 
                    "error": f"GraphQL query failed: HTTP {response.status_code}"
                }
                
        except requests.RequestException as e:
            return {"success": False, "error": f"GraphQL request failed: {str(e)}"}
    
    def query_latest_nodes(self, content_type: str = "article", limit: int = 10, 
                          fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Query latest nodes of a specific type
        
        Args:
            content_type: Content type to query
            limit: Number of nodes to return
            fields: Specific fields to retrieve
            
        Returns:
            Query result with nodes
        """
        fields = fields or ["title", "created", "nid"]
        field_selections = " ".join(fields)
        
        query = f"""
        query {{
          nodeQuery(filter: {{
            conditions: [
              {{field: "type", value: "{content_type}"}},
              {{field: "status", value: "1"}}
            ]
          }}, sort: [{{field: "created", direction: DESC}}], limit: {limit}) {{
            entities {{
              ... on Node{content_type.title()} {{
                {field_selections}
              }}
            }}
          }}
        }}
        """
        
        return self.execute_query(query)
    
    def search_nodes(self, search_term: str, content_type: str = "article", 
                    limit: int = 10) -> Dict[str, Any]:
        """
        Search nodes by title or content
        
        Args:
            search_term: Term to search for
            content_type: Content type to search within
            limit: Number of results to return
            
        Returns:
            Search results
        """
        query = f"""
        query {{
          nodeQuery(filter: {{
            conditions: [
              {{field: "type", value: "{content_type}"}},
              {{field: "title", value: "{search_term}", operator: CONTAINS}},
              {{field: "status", value: "1"}}
            ]
          }}, limit: {limit}) {{
            entities {{
              ... on Node{content_type.title()} {{
                title
                nid
                created
                body {{
                  value
                }}
              }}
            }}
          }}
        }}
        """
        
        return self.execute_query(query)
    
    def query_users_by_role(self, role: str, limit: int = 10) -> Dict[str, Any]:
        """
        Query users by role
        
        Args:
            role: User role to filter by
            limit: Number of users to return
            
        Returns:
            User query results
        """
        query = f"""
        query {{
          userQuery(filter: {{
            conditions: [
              {{field: "roles", value: "{role}"}}
            ]
          }}, limit: {limit}) {{
            entities {{
              name
              mail
              uid
              created
            }}
          }}
        }}
        """
        
        return self.execute_query(query)
    
    def query_taxonomy_terms(self, vocabulary: str, limit: int = 50) -> Dict[str, Any]:
        """
        Query taxonomy terms from a vocabulary
        
        Args:
            vocabulary: Vocabulary machine name
            limit: Number of terms to return
            
        Returns:
            Taxonomy terms
        """
        query = f"""
        query {{
          taxonomyTermQuery(filter: {{
            conditions: [
              {{field: "vid", value: "{vocabulary}"}}
            ]
          }}, limit: {limit}) {{
            entities {{
              name
              tid
              description {{
                value
              }}
            }}
          }}
        }}
        """
        
        return self.execute_query(query)
    
    def query_nodes_with_tags(self, tags: List[str], content_type: str = "article", 
                             limit: int = 10) -> Dict[str, Any]:
        """
        Query nodes that have specific taxonomy tags
        
        Args:
            tags: List of tag names
            content_type: Content type to query
            limit: Number of nodes to return
            
        Returns:
            Tagged nodes
        """
        # Convert tags list to GraphQL array format
        tags_condition = ', '.join([f'"{tag}"' for tag in tags])
        
        query = f"""
        query {{
          nodeQuery(filter: {{
            conditions: [
              {{field: "type", value: "{content_type}"}},
              {{field: "field_tags.name", value: [{tags_condition}], operator: IN}},
              {{field: "status", value: "1"}}
            ]
          }}, limit: {limit}) {{
            entities {{
              ... on Node{content_type.title()} {{
                title
                nid
                created
                fieldTags {{
                  entity {{
                    name
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        
        return self.execute_query(query)
