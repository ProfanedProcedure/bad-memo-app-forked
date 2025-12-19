"""教材用: いろいろ臭いメモエクスポートスクリプト

実行:
python tools/export_memos.py
"""

import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "memo_project.settings")

import django
django.setup()

from memos.models import Memo  # noqa

def main():
    out = []
    memos = Memo.objects.all()
    for m in memos:
        out.append({
            "id": m.id,
            "title": m.title,
            "body": m.body,
            "tags": [t.name for t in m.tags.all()],
        })

    with open("memo_export.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=2))

    print("exported:", len(out))

if __name__ == "__main__":
    main()
