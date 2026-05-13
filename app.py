import streamlit as st
import Main  # ملفك الأصلي الذي يحتوي على منطق الـ VIP والـ Threshold
from datetime import datetime

# إعدادات النظام الرسمية
st.set_page_config(page_title="نظام إدارة المبيعات الموحد", page_icon="🖥️", layout="wide")

# تصميم الواجهة الاحترافية
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    div.stButton > button:first-child { background-color: #002b5c; color: white; border-radius: 8px; font-weight: bold; }
    .invoice-card { padding: 25px; border-radius: 12px; border-right: 8px solid #28a745; background-color: #ffffff; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# البيانات الأساسية
products = Main.all_products
customers = Main.all_customers

with st.sidebar:
    st.header("⚙️ إعدادات النظام")
    # إضافة ميزة التحكم في VIP Threshold مباشرة من الواجهة
    current_threshold = getattr(Main, 'vip_threshold', 500.0) 
    new_threshold = st.number_input("تعديل حد الـ VIP (Threshold)", min_value=0.0, value=float(current_threshold))
    if st.button("تحديث الحد"):
        Main.vip_threshold = new_threshold
        st.success(f"تم تحديث الحد إلى {new_threshold}")
    st.divider()
    st.caption(f"نظام ERP المطور - {datetime.now().strftime('%Y-%m-%d')}")

tab_order, tab_admin = st.tabs(["🛒 معالجة طلب جديد", "📊 إدارة السجلات والمخزون"])

with tab_order:
    col_in, col_out = st.columns([1, 1], gap="large")
    with col_in:
        st.subheader("إدخال بيانات العملية")
        c_name = st.selectbox("قاعدة بيانات العملاء", [c.name for c in customers], index=None)
        p_name = st.selectbox("دليل المنتجات المتاحة", [p.name for p in products], index=None)
        qty = st.number_input("الكمية", min_value=1, step=1)
        
        if st.button("تأكيد العملية وإصدار الفاتورة"):
            if c_name and p_name:
                customer = next(c for c in customers if c.name == c_name)
                product = next(p for p in products if p.name == p_name)
                
                if qty <= product.stock:
                    # 1. حساب المجموع الأساسي
                    subtotal = float(product.price) * qty
                    
                    # 2. استدعاء دالة الخscم الفعلية من الكلاس (لضمان تطبيق خصم الـ VIP)
                    discount_val = customer.get_discount(subtotal)
                    
                    # 3. معالجة القيمة المرتجعة (سواء كانت الخصم نفسه أو السعر الجديد)
                    if discount_val > subtotal: # إذا رجعت الدالة السعر بعد الخصم
                        final_price = discount_val
                        applied_disc = subtotal - final_price
                    else:
                        applied_disc = discount_val
                        final_price = subtotal - applied_disc

                    # 4. تحديث المخزون
                    product.update_stock(qty)
                    
                    # 5. عرض الفاتورة بشكل رسمي
                    st.balloons()
                    st.markdown(f"""
                    <div class="invoice-card">
                        <h4 style="color: #002b5c;">🧾 فاتورة ضريبية معتمدة</h4>
                        <hr>
                        <p><b>المستفيد:</b> {customer.name} (<span style="color: green;">{type(customer).__name__}</span>)</p>
                        <p><b>البيان:</b> {product.name} (عدد {qty})</p>
                        <p>إجمالي القيمة: {subtotal:,.2f} SAR</p>
                        <p style="color: #d9534f;">الخصم المطبق: -{applied_disc:,.2f} SAR</p>
                        <h2 style="color: #28a745;">الصافي: {final_price:,.2f} SAR</h2>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("المخزون غير كافٍ")

with tab_admin:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📦 المخزون")
        st.table([{"المنتج": p.name, "المخزون": p.stock} for p in products])
    with c2:
        st.subheader("👥 سجل العملاء")
        # عرض حالة العميل الحالية لتعرف من هو VIP ومن هو Member
        st.table([{"الاسم": c.name, "الفئة": type(c).__name__} for c in customers])
