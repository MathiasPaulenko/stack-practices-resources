"""Tests for argparse and Click CLI examples."""

import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from argparse_example import build_parser


class TestArgparseExample:
    def test_basic_args(self):
        parser = build_parser()
        args = parser.parse_args(["input.txt"])
        assert args.input == "input.txt"
        assert args.output == "out.txt"
        assert args.verbose is False

    def test_output_flag(self):
        parser = build_parser()
        args = parser.parse_args(["input.txt", "-o", "custom.txt"])
        assert args.output == "custom.txt"

    def test_verbose_flag(self):
        parser = build_parser()
        args = parser.parse_args(["input.txt", "-v"])
        assert args.verbose is True

    def test_count_type_validation(self):
        parser = build_parser()
        args = parser.parse_args(["input.txt", "--count", "5"])
        assert args.count == 5
        assert isinstance(args.count, int)

    def test_push_subcommand(self):
        parser = build_parser()
        args = parser.parse_args(["input.txt", "push", "--force"])
        assert args.command == "push"

    def test_pull_subcommand_with_depth(self):
        parser = build_parser()
        args = parser.parse_args(["input.txt", "pull", "--depth", "3"])
        assert args.command == "pull"

    def test_missing_required_arg_exits_nonzero(self):
        parser = build_parser()
        try:
            parser.parse_args([])
            assert False, "Should have raised SystemExit"
        except SystemExit as e:
            assert e.code == 2


class TestClickExample:
    def test_click_available(self):
        try:
            import click
            assert click is not None
        except ImportError:
            import pytest
            pytest.skip("Click not installed")
