import re
from collections import Counter, defaultdict

def load_articles_by_category(path):
    category_articles = defaultdict(list)
    current_category = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                current_category = line.strip().replace("## ", "")
            elif line.strip().startswith("- **") and current_category:
                title = re.sub(r"[\-*•]+", "", line).strip()
                category_articles[current_category].append(title)
    return category_articles

def extract_keywords(texts):
    all_words = []
    for text in texts:
        # 한글 단어만 추출
        words = re.findall(r"[가-힣]{2,}", text)
        all_words.extend(words)
    counter = Counter(all_words)
    return counter.most_common(20)

def update_categories_file(category_keywords):
    if not os.path.exists("categories.txt"):
        return

    with open("categories.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    cat_dict = {}
    for line in lines:
        if ':' in line:
            cat, kws = line.strip().split(":", 1)
            cat_dict[cat] = set(k.strip() for k in kws.split(","))

    for cat, keywords in category_keywords.items():
        if cat not in cat_dict:
            cat_dict[cat] = set()
        cat_dict[cat].update(keywords)

    with open("categories.txt", "w", encoding="utf-8") as f:
        for cat, kws in sorted(cat_dict.items()):
            f.write(f"{cat}: {','.join(sorted(set(kws)))}\n")
