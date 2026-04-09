#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import unittest
from collections import Counter

import toml

from gfi.github_urls import parse_github_url

DATA_FILE_PATH = "data/repositories.toml"
LABELS_FILE_PATH = "data/labels.json"


def _get_data_from_toml(file_path):
    with open(file_path, "r") as file_desc:
        return toml.load(file_desc)


def _get_data_from_json(file_path):
    with open(file_path, "r") as file_desc:
        return json.load(file_desc)


class TestDataSanity(unittest.TestCase):
    """Test for sanity of the data file."""

    @staticmethod
    def test_data_file_exists():
        """Verify that the data file exists."""
        assert os.path.exists(DATA_FILE_PATH)

    @staticmethod
    def test_labels_file_exists():
        """Verify that the labels file exists."""
        assert os.path.exists(LABELS_FILE_PATH)

    @staticmethod
    def test_data_file_sane():
        """Verify that the file is a valid TOML with required data."""
        data = _get_data_from_toml(DATA_FILE_PATH)
        assert "repositories" in data

    @staticmethod
    def test_labels_file_sane():
        """Verify that the labels file is a valid JSON"""
        data = _get_data_from_json(LABELS_FILE_PATH)
        assert "labels" in data

    @staticmethod
    def test_no_duplicates():
        """Verify that all entries are unique."""
        data = _get_data_from_toml(DATA_FILE_PATH)
        repos = data.get("repositories", [])
        assert len(repos) == len(set(repos))


class TestGitHubUrlParsing(unittest.TestCase):
    """Test parsing the repository URL formats used by the data file."""

    def test_parse_plain_github_url(self):
        assert parse_github_url("github.com/owner/repo") == {"owner": "owner", "name": "repo"}

    def test_parse_https_github_url(self):
        assert parse_github_url("https://github.com/owner/repo.git") == {
            "owner": "owner",
            "name": "repo",
        }

    def test_parse_ssh_github_url(self):
        assert parse_github_url("git@github.com:owner/repo.git") == {"owner": "owner", "name": "repo"}

    def test_reject_non_github_url(self):
        assert parse_github_url("https://example.com/owner/repo") == {}


if __name__ == "__main__":
    unittest.main()
