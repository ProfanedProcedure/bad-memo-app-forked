#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "memo_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django の import に失敗しました。仮想環境と requirements.txt を確認してください。") from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
