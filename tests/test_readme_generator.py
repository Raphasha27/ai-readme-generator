"""Tests for ai_readme_generator."""
import pytest
from unittest.mock import patch, MagicMock
from ai_readme_generator import query_ollama, scan_codebase
from pathlib import Path

class TestScanCodebase:
    def test_finds_python_files(self, tmp_path):
        (tmp_path / "main.py").write_text("print('hello')")
        (tmp_path / "utils.py").write_text("def util(): pass")
        (tmp_path / ".git").mkdir()
        result = scan_codebase(tmp_path)
        assert "main.py" in result
        assert "utils.py" in result

    def test_ignores_git(self, tmp_path):
        (tmp_path / "main.py").write_text("code")
        (tmp_path / ".git" / "config").mkdir(parents=True)
        (tmp_path / ".git" / "objects" / "pack").mkdir(parents=True)
        result = scan_codebase(tmp_path)
        assert ".git" not in result

    def test_empty_directory(self, tmp_path):
        result = scan_codebase(tmp_path)
        assert isinstance(result, str)

class TestQueryOllama:
    def test_generates_readme(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"response": "# Project\n\n## Description\n..."}
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_resp
            result = query_ollama("codebase content")
            assert "# Project" in result

    def test_error_handling(self):
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = TimeoutError
            result = query_ollama("code")
            assert "Error" in result
