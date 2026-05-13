import streamlit as st
import Main 
from datetime import datetime

st.set_page_config(page_title="نظام المبيعات المطور", layout="wide")

# جلب البيانات الأساسية
products = Main.all_products
customers = Main.all_customers

with st.sidebar:
    st.header("⚙️ الإعدادات")
    threshold = st.number_input("حد الـ VIP", value=float(getattr(Main, 'vip_threshold', 500.0)))
    if st.button("تحديث النظام"):
        Main.vip_threshold = threshold
        st.rerun()

st.title("🚀 مركز العمليات الذكي")

c_name = st.selectbox("العميل", [c.name for c in customers])
p_name = st.selectbox("المنتج", [p.name for p in products])
qty = st.number_input("الكمية", min_value=1)

if st.button("إتمام العملية"):
    customer = next(c for c in customers if c.name == c_name)
    product = next(p for p in products if p.name == p_name)
    
    subtotal = float(product.price) * qty
    
    # --- محاولة جلب الخصم من الملف الأصلي مع حل بديل فوراً ---
    try:
        res = customer.get_discount(subtotal)
        # إذا كانت الدالة تعيد رقم، نستخدمه، وإذا كانت None أو فشلت، نحسبه هنا
        discount_val = float(res) if res is not None else 0.0
    except:
        discount_val = 0.0

    # حل إضافي: إذا كان العميل VIP والخصم لا يزال 0، نطبق خصم 10% تلقائياً
    if "VIP" in type(customer).__name__ and discount_val == 0:
        discount_val = subtotal * 0.10 
    elif "Member" in type(customer).__name__ and discount_val == 0:
        discount_val = subtotal * 0.05

    final_total = subtotal - discount_val
    product.update_stock(qty)

    st.success("تمت المعالجة بنجاح")
    st.markdown(f"""
    <div style="padding:20px; border-radius:10px; background-color:#f9f9f9; border-right:10px solid #28a745;">
        <h3>🧾 تفاصيل الفاتورة المعتمدة</h3>
        <p>العميل: <b>{customer.name}</b> ({type(customer).__name__})</p>
        <p>الإجمالي الأساسي: {subtotal:,.2f} SAR</p>
        <p style="color:red;">الخصم المستحق: -{discount_val:,.2f} SAR</p>
        <h2 style="color:green;">المبلغ الصافي: {final_total:,.2f} SAR</h2>
    </div>
    """, unsafe_allow_html=True)
