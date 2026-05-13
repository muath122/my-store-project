import streamlit as st
import Main  # استدعاء ملفك الأصلي
from datetime import datetime

# إعدادات الواجهة
st.set_page_config(page_title="نظام مبيعات المتجر الإلكتروني", layout="wide")

# جلب البيانات من ملفك الأصلي
products = Main.all_products
customers = Main.all_customers

# تصميم بسيط وواضح
st.markdown("""
    <style>
    .invoice-box { padding: 20px; border-radius: 10px; border: 2px solid #28a745; background-color: #fdfdfd; }
    .price-text { font-size: 24px; color: #28a745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ إعدادات النظام")
    # التأكد من مطابقة الـ Threshold المستخدم في التيرمنال
    t_val = st.number_input("VIP Threshold", value=float(getattr(Main, 'vip_threshold', 500.0)))
    Main.vip_threshold = t_val 
    st.info(f"الحد الحالي للترقية: {t_val} SAR")

st.title("🛍️ معالجة الطلبات (مطابق لمخرجات النظام)")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("إدخال البيانات")
    c_name = st.selectbox("اختر العميل", [c.name for c in customers])
    p_name = st.selectbox("اختر المنتج", [p.name for p in products])
    qty = st.number_input("الكمية", min_value=1, step=1)
    
    if st.button("إتمام العملية وحساب الخصم"):
        customer = next(c for c in customers if c.name == c_name)
        product = next(p for p in products if p.name == p_name)
        
        # 1. الحساب الأساسي
        subtotal = float(product.price) * qty
        
        # 2. تحديث حالة العميل (للتأكد من تحوله لـ VIP قبل الخصم)
        # ملاحظة: استدعاء الدالة كما هي في Main.py
        customer.get_discount(subtotal) 
        
        # 3. جلب القيمة النهائية للخصم بعد الترقية
        # قمنا بتحويلها لـ float لضمان عدم حدوث TypeError
        raw_discount = customer.get_discount(subtotal)
        try:
            discount_val = float(raw_discount) if raw_discount is not None else 0.0
        except:
            discount_val = 0.0

        # 4. حساب الصافي النهائي
        # إذا كانت الدالة تعيد السعر النهائي (مثل 2550)
        if discount_val > subtotal: 
            final_total = discount_val
            applied_disc = subtotal - final_total
        else:
            # إذا كانت الدالة تعيد قيمة الخصم (مثل 450)
            applied_disc = discount_val
            final_total = subtotal - applied_disc

        # تحديث المخزون في النظام
        product.update_stock(qty)
        
        with col2:
            st.subheader("المخرجات النهائية")
            st.markdown(f"""
            <div class="invoice-box">
                <h4>🧾 فاتورة النظام الموحد</h4>
                <p><b>اسم العميل:</b> {customer.name}</p>
                <p><b>فئة العميل برمجياً:</b> <span style="color:blue;">{type(customer).__name__}</span></p>
                <hr>
                <p>المجموع قبل الخصم: {subtotal:,.2f} SAR</p>
                <p style="color:red;">خصم الفئة المطبق: -{applied_disc:,.2f} SAR</p>
                <p class="price-text">الصافي المطلوب: {final_total:,.2f} SAR</p>
            </div>
            """, unsafe_allow_html=True)
            
            if "VIP" in type(customer).__name__:
                st.success("✨ تم تطبيق خصم الـ VIP بنجاح (مطابق للتيرمنال)")
