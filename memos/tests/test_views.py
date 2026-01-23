from django.test import TestCase
from django.urls import reverse
from memos.models import Memo

class MemoViewTests(TestCase):
    def test_list_page_ok(self):
        res = self.client.get(reverse("memo_list"))
        self.assertEqual(res.status_code, 200)

    def test_create_requires_title(self):
        res = self.client.post(reverse("create_memo"), data={"title": "", "body": "x", "tags": ""})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "タイトルは必須")

    def test_detail_nonexistent_memo_returns_404(self):
        # Test that accessing a non-existent memo returns 404
        res = self.client.get(reverse("memo_detail", args=[99999]))
        self.assertEqual(res.status_code, 404)

    def test_edit_nonexistent_memo_returns_404(self):
        # Test that editing a non-existent memo returns 404
        res = self.client.get(reverse("edit_memo", args=[99999]))
        self.assertEqual(res.status_code, 404)

    def test_delete_nonexistent_memo_returns_404(self):
        # Test that deleting a non-existent memo returns 404
        res = self.client.get(reverse("delete_memo", args=[99999]))
        self.assertEqual(res.status_code, 404)

    def test_detail_existing_memo_returns_200(self):
        # Create a memo and verify it can be accessed
        memo = Memo.objects.create(title="Test Memo", body="Test Body")
        res = self.client.get(reverse("memo_detail", args=[memo.id]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Test Memo")

    # TODO: detail/edit/delete / legacy検索 / pagination のテストを追加
