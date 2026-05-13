import streamlit as st
import Main  # استدعاء ملفك الأساسي
from datetime import datetime

# إعدادات النظام الاحترافية
st.set_page_config(page_title="نظام الإدارة المالية الموحد", page_icon="🖥️", layout="wide")

# تصميم الواجهة (Custom CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    div.stButton > button:first-child { background-color: #002b5c; color: white; border-radius: 8px; font-weight: bold; }
    .invoice-card { padding: 25px; border-radius: 12px; border-right: 10px solid #28a745; background-color: #ffffff; box-shadow: 0 10px 20px rgba(0,0,0,0.05); color: #333; }
    </style>
    """, unsafe_allow_html=True)

# جلب البيانات والتأكد من وجودها
products = getattr(Main, 'all_products', [])
customers = getattr(Main, 'all_customers', [])

with st.sidebar:
    st.header("⚙️ لوحة التحكم الإدارية")
    # عرض وتعديل حد الـ VIP (Threshold)
    current_threshold = getattr(Main, 'vip_threshold', 500.0)
    new_threshold = st.number_input("تعديل سقف الـ VIP (Threshold)", min_value=0.0, value=float(current_threshold))
    if st.button("تحديث إعدادات النظام"):
        Main.vip_threshold = new_threshold
        st.success(f"تم تحديث الحد إلى {new_threshold}")
    st.divider()
    st.caption(f"نظام إدارة الموارد - {datetime.now().strftime('%Y-%m-%d')}")

tab_order, tab_admin = st.tabs(["🛒 معالجة طلب جديد", "📊 سجلات الإدارة"])

with tab_order:
    col_in, col_out = st.columns([1, 1], gap="large")
    with col_in:
        st.subheader("بيانات العملية التجارية")
        c_name = st.selectbox("قاعدة بيانات العملاء", [c.name for c in customers], index=None, placeholder="اختر العميل...")
        p_name = st.selectbox("دليل المنتجات", [p.name for p in products], index=None, placeholder="اختر المنتج...")
        qty = st.number_input("الكمية المطلوبة", min_value=1, step=1)
        
        if st.button("اعتماد العملية وإصدار الفاتورة"):
            if c_name and p_name:
                customer = next(c for c in customers if c.name == c_name)
                product = next(p for p in products if p.name == p_name)
                
                if qty <= product.stock:
                    # حساب المجموع
                    subtotal = float(product.price) * qty
                    
                    # استدعاء دالة الخصم ومعالجة القيمة المرتجعة (الحل الجذري للـ TypeError)
                    raw_discount = customer.get_discount(subtotal)
                    
                    # التأكد من تحويل القيمة لرقم مهما كان نوعها
                    try:
                        discount_val = float(raw_discount) if raw_discount is not None else 0.0
                    except (TypeError, ValueError):
                        discount_val = 0.0

                    # منطق احتساب الخصم (إذا كانت الدالة تعيد السعر الجديد أو قيمة الخصم)
                    if 0 < discount_val < subtotal:
                        applied_disc = discount_val
                        final_price = subtotal - applied_disc
                    elif discount_val >= subtotal:
                        final_price = discount_val
                        applied_disc = subtotal - final_price
                    else:
                        applied_disc = 0.0
                        final_price = subtotal

                    product.update_stock(qty)
                    
                    st.balloons()
                    st.markdown(f"""
                    <div class="invoice-card">
                        <h3 style="color: #002b5c; margin-top: 0;">🧾 فاتورة ضريبية معتمدة</h3>
                        <hr>
                        <p><b>العميل:</b> {customer.name} (<span style="color: #002b5c;">{type(customer).__name__}</span>)</p>
                        <p><b>المنتج:</b> {product.name} (عدد {qty})</p>
                        <p style="font-size: 1.1em;">الإجمالي قبل الخصم: <b>{subtotal:,.2f} SAR</b></p>
                        <p style="color: #d9534f; font-size: 1.1em;">قيمة الخصم المطبق: <b>-{applied_disc:,.2f} SAR</b></p>
                        <h2 style="color: #28a745;">صافي المبلغ: {final_price:,.2f} SAR</h2>
                        <p style="font-size: 0.8em; color: gray; margin-bottom: 0;">صدرت آلياً برقم مرجع: {datetime.now().strftime('%H%M%S')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"المخزون غير كافٍ (المتاح: {product.stock})")

with tab_admin:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📦 تقرير المخزون")
        st.table([{"المنتج": p.name, "المخزون": p.stock, "السعر": f"{p.price} SAR"} for p in products])
    with c2:
        st.subheader("👥 سجل الفئات")
        # عرض نوع الكلاس (Member/VIPMember) للتأكد من نظام الـ Threshold
        st.table([{"الاسم": c.name, "الفئة الحالية": type(c).__name__} for c in customers])
