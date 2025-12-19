# バグ・改善ポイント一覧（教材用）

このリポジトリには「見つけて直す」ためのポイントが複数入っています。  
難易度は★〜★★★。授業では **★→★★→★★★** の順に進めるのがおすすめです。

---

## セキュリティ / 安全性

### ★★★ 旧検索(legacy=1)が生SQL文字列連結（壊れやすい・危険）
- 場所：`memos/views.py` の `memo_list()`（legacy分岐）
- 症状：検索語に `'` を含むと落ちやすい / 期待しない動作になりやすい
- 直し方：ORMで書く（推奨） / どうしても raw を使うなら **安全な形**へ

### ★★ delete が POST 限定になっていない
- 場所：`memos/views.py` の `delete_memo()`
- 症状：GETで削除できてしまう（意図しない操作につながる）
- 直し方：POSTのみ許可（GETは405など）/ 例外握りつぶしも整理

### ★ get() 直叩きで 404 を返さない
- 場所：`memo_detail()`, `edit_memo()` の `Memo.objects.get(...)`
- 症状：存在しないIDで 500 になりがち
- 直し方：`get_object_or_404` に変更

---

## パフォーマンス / UX

### ★★ ページネーションが無い（一覧が重い・長い）
- 場所：`memo_list()` と `templates/memos/memo_list.html`
- 症状：fixture大量でスクロールが大変
- 直し方：`Paginator` を導入し、GETパラメータを保持したままページ送り

### ★★ N+1 の芽（一覧でタグ表示）
- 場所：`memo_list()`（テンプレで `memo.tags.all`）
- 直し方：`prefetch_related("tags")` を追加

---

## 設計 / 保守性

### ★★ create/edit の重複（コピペ）
- 場所：`create_memo()`, `edit_memo()`
- 直し方：共通処理を関数化 or Form導入で view を薄く

### ★★ Form を使っていない（バリデーションが散在）
- 場所：`create_memo()`, `edit_memo()`, `templates/memos/memo_form.html`
- 直し方：`forms.py` を作り `MemoForm` にバリデーション/正規化を集約

### ★★ タグ処理が雑（例外握りつぶし・重複/正規化）
- 場所：`Memo.attach_tags_from_csv()`
- 直し方：重複排除・例外方針・責務分離（Form/Serviceに寄せるなど）

### ★ export スクリプトが臭い
- 場所：`tools/export_memos.py`
- 直し方：管理コマンド化、引数化、エラーハンドリング、prefetchなど

---

## “追加の見つけやすい課題”スイッチ（v2+）

### ★★ unsafe_sort=1 で order_by にユーザー入力を直渡し（落ちやすい）
- 場所：`memos/views.py` の `memo_list()`（unsafe_sort分岐）
- 症状：想定外の sort 値で 500 になりやすい
- 直し方：許可リスト方式に統一（parse_sort を使うなど）

> ※このスイッチは「入力検証の大切さ」を体験するための教材用です。
