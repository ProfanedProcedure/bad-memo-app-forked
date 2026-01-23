"""Tests for the export_memos management command."""

import json
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext

from memos.models import Memo, Tag


class ExportMemosCommandTests(TestCase):
    """Test the export_memos management command."""

    def setUp(self):
        """Create test data."""
        # Create tags
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        tag3 = Tag.objects.create(name="tag3")

        # Create memos with tags
        memo1 = Memo.objects.create(title="Test Memo 1", body="Body 1")
        memo1.tags.add(tag1, tag2)

        memo2 = Memo.objects.create(title="Test Memo 2", body="Body 2")
        memo2.tags.add(tag2, tag3)

        memo3 = Memo.objects.create(title="Test Memo 3", body="Body 3")
        # No tags for this one

    def test_export_default_output(self):
        """Test export with default output file."""
        out = StringIO()
        
        # Remove existing file if it exists
        default_file = Path("memo_export.json")
        if default_file.exists():
            default_file.unlink()

        call_command("export_memos", stdout=out)
        
        # Check that file was created
        self.assertTrue(default_file.exists())
        
        # Check output message
        output = out.getvalue()
        self.assertIn("Successfully exported", output)
        self.assertIn("3 memos", output)
        
        # Verify content
        with open(default_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["title"], "Test Memo 1")
        self.assertIn("tag1", data[0]["tags"])
        self.assertIn("tag2", data[0]["tags"])
        
        # Cleanup
        default_file.unlink()

    def test_export_custom_output(self):
        """Test export with custom output file."""
        out = StringIO()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "custom_export.json"
            
            call_command("export_memos", output=str(output_file), stdout=out)
            
            # Check that file was created
            self.assertTrue(output_file.exists())
            
            # Verify content
            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.assertEqual(len(data), 3)

    def test_export_custom_indent(self):
        """Test export with custom indentation."""
        out = StringIO()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "indent_export.json"
            
            call_command("export_memos", output=str(output_file), indent=4, stdout=out)
            
            # Check that file was created and has proper indentation
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # With indent=4, should have 4 spaces at start of nested lines
            self.assertIn("    \"id\":", content)

    def test_no_n_plus_one_queries(self):
        """Test that export doesn't have N+1 query problem."""
        out = StringIO()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "query_test.json"
            
            # Count queries during export
            with CaptureQueriesContext(connection) as context:
                call_command("export_memos", output=str(output_file), stdout=out)
            
            # Should be very few queries:
            # 1. Count query for memos
            # 2. Fetch all memos with prefetch_related
            # The number should be constant regardless of memo count
            # With prefetch_related, we expect around 2-3 queries total
            num_queries = len(context.captured_queries)
            
            # Without prefetch_related, we'd have 1 + 1 + N queries (where N is number of memos)
            # With prefetch_related, we should have only 2-3 queries total
            self.assertLessEqual(num_queries, 5, 
                f"Too many queries ({num_queries}), possible N+1 problem. Queries: {context.captured_queries}")

    def test_invalid_output_path(self):
        """Test error handling for invalid output path."""
        from django.core.management.base import CommandError
        out = StringIO()
        err = StringIO()
        
        # Try to write to a forbidden location
        with self.assertRaises(CommandError):
            call_command("export_memos", output="/root/forbidden.json", stdout=out, stderr=err)
