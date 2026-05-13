import streamlit as st
import Main  # الربط المباشر بالكود الأساسي حقنا

st.set_page_config(page_title="نظام إدارة المتجر", layout="wide")

# جلب البيانات من الكود الأساسي
products = Main.all_products
customers = Main.all_customers

# --- الجانب الإداري (Sidebar) ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم الإدارية")
    
    # 1. تحديث سقف الـ VIP
    st.subheader("تحديد الـ VIP Threshold")
    new_threshold = st.number_input("الحد الحالي للترقية", value=float(getattr(Main, 'vip_threshold', 500.0)))
    if st.button("تحديث الحد"):
        Main.vip_threshold = new_threshold
        st.success(f"تم تحديث الحد إلى {new_threshold}")

    st.divider()
    
    # 2. عرض المخزون والعملاء
    tab1, tab2 = st.tabs(["📦 المخزون", "👥 العملاء"])
    
    with tab1:
        for p in products:
            st.write(f"**{p.name}:** {p.stock} قطعة")
            
    with tab2:
        for c in customers:
            st.write(f"**{c.name}** ({type(c).__name__})")

# --- الواجهة الرئيسية (معالجة العمليات) ---
st.title("🛍️ مركز معالجة العمليات")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("بيانات الطلب")
    c_name = st.selectbox("اختر العميل", [c.name for c in customers])
    p_name = st.selectbox("اختر المنتج", [p.name for p in products])
    qty = st.number_input("الكمية", min_value=1, step=1)
    
    if st.button("اعتماد العملية"):
        customer = next(c for c in customers if c.name == c_name)
        product = next(p for p in products if p.name == p_name)
        
        subtotal = product.price * qty
        
        # استدعاء القرار من الكود الأساسي
        final_price = customer.get_discount(subtotal)
        
        # تنفيذ تحديث المخزون من الكود الأساسي
        product.update_stock(qty)
        
        with col2:
            st.header("المخرجات (من النظام)")
            st.success(f"تمت العملية لـ {customer.name} بنجاح")
            
            # عرض النتائج كما في التيرمنال
            st.info(f"المنتج: {product.name} | الكمية: {qty}")
            st.write(f"الإجمالي قبل الخصم: {subtotal:,.2f} SAR")
            
            # التعامل مع مخرجات الكود الأساسي (سواء كانت Return أو Print)
            if final_price is not None:
                st.metric("الصافي المطلوب دفعها", f"{final_price:,.2f} SAR")
            else:
                # في حال كان الكود يطبع فقط، نظهر رسالة تأكيد
                st.warning("القرار تم اتخاذه في النظام (الرجاء مراجعة التيرمنال للرقم الدقيق)")
