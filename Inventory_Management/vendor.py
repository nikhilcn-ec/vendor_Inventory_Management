import streamlit as st


product_catalog=st.Page(
    page="view/product_catalog.py",
    title="product_catalog",
    icon=":material/update:"
)

inventory_management=st.Page(
    page="view/inventory.py",
    title="inventory_management",
    icon=":material/inventory_2:"
)

Dashboard=st.Page(
    page="view/dashboard.py",
    title="dashboard",
    default=True,
    icon=":material/bar_chart_4_bars:"
)

chatbot=st.Page(
    page="view/chatbot.py",
    title="chatbot",
    icon=":material/chat:"
)

pg=st.navigation(pages=[product_catalog,Dashboard,chatbot,inventory_management])
pg.run()


