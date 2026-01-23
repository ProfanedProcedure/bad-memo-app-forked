"""Django management command to export memos to JSON.

Usage:
    python manage.py export_memos [options]
"""

import json
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from memos.models import Memo


class Command(BaseCommand):
    help = "Export memos to JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            "-o",
            type=str,
            default="memo_export.json",
            help="Output file path (default: memo_export.json)",
        )
        parser.add_argument(
            "--indent",
            type=int,
            default=2,
            help="JSON indentation spaces (default: 2)",
        )

    def handle(self, *args, **options):
        output_path = options["output"]
        indent = options["indent"]

        try:
            # Use prefetch_related to avoid N+1 query problem
            memos = Memo.objects.prefetch_related("tags").all()

            # Build export data
            out = []
            for m in memos:
                out.append({
                    "id": m.id,
                    "title": m.title,
                    "body": m.body,
                    "tags": [t.name for t in m.tags.all()],
                })

            self.stdout.write(f"Exporting {len(out)} memos...")

            # Validate output path
            output_file = Path(output_path)
            
            # Create parent directories if they don't exist
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Write to file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=indent)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully exported {len(out)} memos to {output_path}"
                )
            )

        except PermissionError as e:
            raise CommandError(f"Permission denied writing to {output_path}: {e}")
        except OSError as e:
            raise CommandError(f"Failed to write file {output_path}: {e}")
        except Exception as e:
            raise CommandError(f"Unexpected error during export: {e}")
