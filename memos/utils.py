import datetime

# NOTE: 便利そうに見えるけど、薄く責務が混ざっている utility

def now_jst_string():
    # 匂い: timezone 無視でローカル時間を決め打ち
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def normalize_q(q):
    if q is None:
        return ""
    q = q.replace("　", " ").strip()
    while "  " in q:
        q = q.replace("  ", " ")
    return q

def parse_sort(sort):
    if sort == "old":
        return "created_at"
    if sort == "title":
        return "title"
    return "-created_at"
