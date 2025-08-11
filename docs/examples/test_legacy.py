import pytest
from unittest.mock import patch, MagicMock
from main import (
    NLParser, CommandFactory, CreatePostCommand, RunDrushCommand, EditNodeCommand, UploadMediaCommand, CreateSiteCommand,
    QueryNodesCommand, QueryUsersCommand, GraphQLQueryCommand
)

def test_nlparser_create_post():
    parser = NLParser()
    intent, params = parser.parse("Create a blog post about AI in Drupal")
    assert intent == "create-post"
    assert "topic" in params
    assert params["topic"] == "ai in drupal"

def test_nlparser_clear_cache():
    parser = NLParser()
    intent, params = parser.parse("Clear Drupal cache")
    assert intent == "run-drush"
    assert params["command"] == "cache:rebuild"

def test_nlparser_upload_media():
    parser = NLParser()
    intent, params = parser.parse("Upload header.jpg to media library with alt text 'Homepage Banner'")
    assert intent == "upload-media"
    assert params["file_path"] == "header.jpg"
    assert params["alt_text"] == "homepage banner"

def test_nlparser_edit_node():
    parser = NLParser()
    intent, params = parser.parse("Edit the title of node 45 to 'Headless CMS in 2025'")
    assert intent == "edit-node"
    assert params["node_id"] == "45"
    assert params["title"] == "headless cms in 2025"

def test_command_factory():
    cmd = CommandFactory.create_command("create-post", {"topic": "AI"})
    assert isinstance(cmd, CreatePostCommand)
    cmd = CommandFactory.create_command("run-drush", {"command": "cr"})
    assert isinstance(cmd, RunDrushCommand)
    cmd = CommandFactory.create_command("edit-node", {"node_id": "1", "title": "Test"})
    assert isinstance(cmd, EditNodeCommand)
    cmd = CommandFactory.create_command("upload-media", {"file_path": "file.jpg"})
    assert isinstance(cmd, UploadMediaCommand)
    cmd = CommandFactory.create_command("create-site", {"project_name": "mysite"})
    assert isinstance(cmd, CreateSiteCommand)

def test_create_post_command_execute():
    params = {"topic": "AI"}
    cmd = CreatePostCommand(params)
    with patch("main.AIContentGenerator.generate_content", return_value="Test body"), \
         patch("main.DrupalAPI.create_node", return_value={"success": True, "node_id": 1, "url": "http://localhost/node/1"}):
        result = cmd.execute()
        assert result["success"] is True
        assert result["data"]["node_id"] == 1

def test_run_drush_command_execute():
    params = {"command": "cr"}
    cmd = RunDrushCommand(params)
    with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout="ok", stderr="")):
        result = cmd.execute()
        assert result["success"] is True
        assert "stdout" in result["data"]

def test_edit_node_command_execute():
    params = {"node_id": "1", "title": "New Title"}
    cmd = EditNodeCommand(params)
    with patch("main.DrupalAPI.update_node", return_value={"success": True, "node_id": 1}):
        result = cmd.execute()
        assert result["success"] is True
        assert result["data"]["node_id"] == 1

def test_upload_media_command_execute():
    params = {"file_path": "file.jpg", "alt_text": "Banner"}
    cmd = UploadMediaCommand(params)
    with patch("main.DrupalAPI.upload_media", return_value={"success": True}):
        result = cmd.execute()
        assert result["success"] is True

def test_create_site_command_execute_ddev():
    params = {"project_name": "mysite", "platform": "ddev"}
    cmd = CreateSiteCommand(params)
    with patch("main.CreateSiteCommand._create_ddev_site", return_value={"success": True, "data": {"project_name": "mysite"}}):
        result = cmd.execute()
        assert result["success"] is True

def test_create_site_command_execute_lando():
    params = {"project_name": "mysite", "platform": "lando"}
    cmd = CreateSiteCommand(params)
    with patch("main.CreateSiteCommand._create_lando_site", return_value={"success": True, "data": {"project_name": "mysite"}}):
        result = cmd.execute()
        assert result["success"] is True

def test_nlparser_query_latest_posts():
    parser = NLParser()
    intent, params = parser.parse("Show me the titles of the latest 10 blog posts")
    assert intent == "query-nodes"
    assert params["content_type"] == "article"
    assert params["limit"] == 10

def test_nlparser_query_users_by_role():
    parser = NLParser()
    intent, params = parser.parse("Get all users with role 'editor'")
    assert intent == "query-users"
    assert params["role"] == "editor"

def test_nlparser_search_content():
    parser = NLParser()
    intent, params = parser.parse("Fetch article bodies containing the word 'Drupal'")
    assert intent == "query-nodes"
    assert params["search_term"] == "drupal"

def test_query_nodes_command_execute():
    params = {"content_type": "article", "limit": 5}
    cmd = QueryNodesCommand(params)
    mock_nodes = [{"id": 1, "title": "Test Post", "type": "node--article"}]
    with patch("main.DrupalAPI.query_nodes", return_value={"success": True, "nodes": mock_nodes}):
        result = cmd.execute()
        assert result["success"] is True
        assert result["data"]["count"] == 1

def test_query_users_command_execute():
    params = {"role": "editor", "limit": 10}
    cmd = QueryUsersCommand(params)
    mock_users = [{"id": 1, "name": "Test User", "email": "test@example.com"}]
    with patch("main.DrupalAPI.query_users", return_value={"success": True, "users": mock_users}):
        result = cmd.execute()
        assert result["success"] is True
        assert result["data"]["count"] == 1

def test_graphql_query_command_execute():
    params = {"query": "{ nodeQuery { entities { title } } }"}
    cmd = GraphQLQueryCommand(params)
    mock_response = {"data": {"nodeQuery": {"entities": [{"title": "Test"}]}}}
    with patch("main.DrupalAPI.graphql_query", return_value={"success": True, "data": mock_response}):
        result = cmd.execute()
        assert result["success"] is True
        assert "data" in result["data"]
