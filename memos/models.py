from django.db import models

# NOTE: 教材用。わざと“匂う”実装が入っています。

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name

class Memo(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="memos")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 匂いポイント: モデルに表示用処理が混ざる / ルールが散在
    def preview(self) -> str:
        text = (self.body or "").replace("\r\n", "\n").replace("\r", "\n")
        text = text.strip()
        if len(text) == 0:
            return "(本文なし)"
        if len(text) > 120:  # magic number
            return text[:120] + "..."
        return text

    def attach_tags_from_csv(self, tag_csv: str):
        # 匂いポイント: “csv” なのにカンマ区切りのみ / 文字処理が雑 / 例外も握りつぶしがち
        if tag_csv is None:
            tag_csv = ""
        pieces = tag_csv.split(",")
        names = []
        for p in pieces:
            x = p.strip()
            if x:
                names.append(x.lower())
        # 重複もまとめず雑に add してみる
        for n in names:
            try:
                t, _ = Tag.objects.get_or_create(name=n)
                self.tags.add(t)
            except Exception:
                # NOTE: 教材用。落ちないが何が起きたか分からない。
                pass
