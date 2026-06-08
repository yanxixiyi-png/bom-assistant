import streamlit as st
import pandas as pd
from tavily import TavilyClient

st.set_page_config(page_title="BOM 智能体助手", page_icon="📦", layout="wide")

TAVILY_API_KEY = "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"

def web_search(query: str) -> str:
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        result = client.search(query, max_results=3)
        if result and result.get('results'):
            output = []
            for i, r in enumerate(result['results'], 1):
                title = r.get('title', '无标题')
                content = r.get('content', '无内容')
                output.append(f"{i}. {title}\n   {content[:300]}...")
            return "\n\n".join(output)
        else:
            return f"未找到关于「{query}」的搜索结果"
    except Exception as e:
        return f"搜索出错：{str(e)}"

st.title("📦 BOM 智能体助手")
st.caption("上传真实 BOM 文件 | 自动解析、统计、筛选、导出 | 支持零件搜索")

if "bom_df" not in st.session_state:
    st.session_state.bom_df = None

with st.sidebar:
    st.header("📂 数据源")
    uploaded_file = st.file_uploader("上传 BOM 文件（CSV 或 Excel）", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.bom_df = df
            st.success(f"✅ 已加载 {len(df)} 条物料")
        except Exception as e:
            st.error(f"文件读取失败：{e}")

    if st.session_state.bom_df is not None:
        st.divider()
        st.header("⚙️ 统计")
        df = st.session_state.bom_df
        if "数量" in df.columns:
            total_qty = df["数量"].sum()
            st.metric("总数量", f"{total_qty} 个")
        if "单重(kg)" in df.columns and "数量" in df.columns:
            total_weight = (df["数量"] * df["单重(kg)"]).sum()
            st.metric("总重量", f"{total_weight:.2f} kg")
        if "材质" in df.columns:
            st.subheader("🔍 筛选")
            materials = ["全部"] + list(df["材质"].dropna().unique())
            selected_material = st.selectbox("按材质筛选", materials)
        st.subheader("📎 导出")
        csv_export = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("下载 CSV", csv_export, "bom_export.csv", "text/csv")

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.bom_df is not None:
        df = st.session_state.bom_df
        if "材质" in df.columns and selected_material != "全部":
            df_display = df[df["材质"] == selected_material]
            st.caption(f"当前显示：{selected_material} ({len(df_display)} 项)")
        else:
            df_display = df
        st.subheader("📋 BOM 物料清单")
        st.dataframe(df_display, use_container_width=True, height=400)
    else:
        st.info("👈 请先在左侧上传 BOM 文件")

with col2:
    st.subheader("🔎 零件搜索助手")
    search_query = st.text_input("输入零件号或名称", placeholder="例如：M12 螺栓 重量")
    if search_query:
        with st.spinner("搜索中..."):
            result = web_search(search_query)
            st.markdown("**搜索结果：**")
            st.write(result)

st.divider()
st.caption("💡 功能：上传真实文件 | 自动解析 | 统计筛选 | CSV导出 | 联网搜索零件信息")
