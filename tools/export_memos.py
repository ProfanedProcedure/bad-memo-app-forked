"""教材用: このスクリプトは非推奨です

このスクリプトには以下の問題がありました:
1. N+1クエリ問題 (prefetch_relatedが無い)
2. エラーハンドリングが無い
3. ファイル名が固定
4. Django管理コマンドではない
5. 引数が無い

新しい実装を使用してください:
python manage.py export_memos [--output PATH] [--indent N]

例:
python manage.py export_memos
python manage.py export_memos --output /tmp/memos.json
python manage.py export_memos --output exports/backup.json --indent 4
"""

import sys

def main():
    print("このスクリプトは非推奨です。")
    print("代わりに以下のコマンドを使用してください:")
    print("  python manage.py export_memos --help")
    sys.exit(1)

if __name__ == "__main__":
    main()
