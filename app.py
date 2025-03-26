import streamlit as st
import os
import datetime
from keyword_learning import load_articles_by_category, extract_keywords, update_categories_file

st.set_page_config(page_title="간단 뉴스 키워드 승인", layout="wide")

st.title("📰 간단 뉴스 키워드 추출 및 승인")

today = datetime.date.today().strftime("%Y-%m-%d")
file_path = f"output/{today}-news.md"

if not os.path.exists(file_path):
    st.warning(f"오늘 뉴스 파일이 없습니다: {file_path}")
else:
    st.info("카테고리별로 추천된 키워드를 확인하고 승인하세요.")

    articles_by_category = load_articles_by_category(file_path)
    selected_keywords = {}

    for cat, articles in articles_by_category.items():
        st.subheader(f"[{cat}]")
        top_keywords = [word for word, _ in extract_keywords(articles)][:10]
        default_select = top_keywords[:3]
        selected = st.multiselect(f"{cat} 키워드 선택", top_keywords, default=default_select, key=cat)
        selected_keywords[cat] = selected

    if st.button("✅ 선택한 키워드를 반영하기"):
        update_categories_file(selected_keywords)
        st.success("카테고리에 키워드가 반영되었습니다!")
