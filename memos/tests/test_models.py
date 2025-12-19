from django.test import TestCase
from memos.models import Memo

class MemoModelTests(TestCase):
    def test_preview_empty(self):
        m = Memo(title="t", body="")
        self.assertEqual(m.preview(), "(本文なし)")

    # TODO: preview の長さ制限や改行処理のテストを追加
