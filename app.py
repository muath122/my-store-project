import streamlit as st
import Main  # استدعاء ملفك الأساسي
from datetime import datetime

# إعدادات النظام
st.set_page_config(page_title="نظام الإدارة المالية الموحد", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .invoice-card { padding: 20px; border-radius: 10px; border-left: 10px solid #28a745; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #333; }
    </style>
    """, unsafe_allow_html=True)

# جلب البيانات
products = Main.all_products
customers = Main.all_customers

with st.sidebar:
    st.header("⚙️ الإعدادات الإدارية")
    # التأكد من جلب سقف الـ VIP الحالي
    current_threshold = getattr(Main, 'vip_threshold', 500.0)
    new_threshold = st.number_input("تعديل سقف الـ VIP (Threshold)", value=float(current_threshold))
    if st.button("تحديث السقف"):
        Main.vip_threshold = new_threshold
        st.success(f"تم التحديث إلى {new_threshold}")

st.title("🛒 مركز معالجة العمليات")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("بيانات الطلب")
    c_name = st.selectbox("اختر العميل", [c.name for c in customers])
    p_name = st.selectbox("اختر المنتج", [p.name for p in products])
    qty = st.number_input("الكمية", min_value=1, step=1)
    
    if st.button("اعتماد العملية"):
        customer = next(c for c in customers if c.name == c_name)
        product = next(p for p in products if p.name == p_name)
        
        # --- الجزء الأهم: تحديث حالة العميل قبل الحساب ---
        subtotal = float(product.price) * qty
        
        # استدعاء دالة الخصم من ملفك الأصلي
        # ملاحظة: تأكد أن دالة get_discount في Main.py ترجع (قيمة الخصم كرقّم)
        raw_discount = customer.get_discount(subtotal)
        
        # معالجة القيمة لضمان عدم حدوث TypeError (كما في الصور السابقة)
        try:
            discount_amount = float(raw_discount) if raw_discount is not None else 0.0
        except:
            discount_amount = 0.0
            
        # إذا كان الخصم المرتجع هو السعر النهائي، نقوم بتعديله
        if discount_amount > subtotal:
            final_total = discount_amount
            applied_disc = subtotal - final_total
        else:
            applied_disc = discount_amount
            final_total = subtotal - applied_disc

        # تحديث المخزون
        product.update_stock(qty)
        
        with col2:
            st.subheader("المخرجات")
            st.markdown(f"""
            <div class="invoice-card">
                <h3>🧾 فاتورة معتمدة</h3>
                <p><b>العميل:</b> {customer.name} (<span style="color:blue;">{type(customer).__name__}</span>)</p>
                <p><b>المنتج:</b> {product.name}</p>
                <hr>
                <p>الإجمالي قبل الخصم: {subtotal:,.2f} SAR</p>
                <p style="color:red;">الخصم المستحق: -{applied_disc:,.2f} SAR</p>
                <h2 style="color:green;">الصافي: {final_total:,.2f} SAR</h2>
            </div>
            """, unsafe_allow_html=True)
