import streamlit as st
import Main  # الربط الأساسي

st.set_page_config(page_title="نظام المتجر", layout="wide")

# --- الجانب الإداري (المميزات المطلوبة) ---
with st.sidebar:
    st.header("⚙️ الإعدادات والمخزون")
    
    # 1. تحديد الـ VIP Threshold
    st.subheader("تعديل سقف الـ VIP")
    new_threshold = st.number_input("الحد الحالي", value=500.0)
    if st.button("تحديث السقف"):
        Main.vip_threshold = new_threshold
        st.success("تم التحديث")

    st.divider()
    
    # 2. عرض العملاء والمخزون
    col_inv1, col_inv2 = st.columns(2)
    with col_inv1:
        st.write("📦 **المخزون:**")
        for p in Main.all_products:
            st.caption(f"{p.name}: {p.stock}")
    with col_inv2:
        st.write("👥 **العملاء:**")
        for c in Main.all_customers:
            st.caption(f"{c.name}")

# --- الواجهة الرئيسية (إدخال الطلب وطباعة الفاتورة) ---
st.title("🛍️ مركز معالجة العمليات")

c_name = st.selectbox("اختر العميل", [c.name for c in Main.all_customers])
p_name = st.selectbox("اختر المنتج", [p.name for p in Main.all_products])
qty = st.number_input("الكمية", min_value=1, step=1)

if st.button("تنفيذ العملية وطباعة الفاتورة"):
    customer = next(c for c in Main.all_customers if c.name == c_name)
    product = next(p for p in Main.all_products if p.name == p_name)
    
    subtotal = product.price * qty
    
    # استدعاء الدوال من كودك الأصلي
    result = customer.get_discount(subtotal)
    product.update_stock(qty)
    
    # --- منطقة طباعة الفاتورة ---
    st.markdown("---")
    st.subheader("🧾 فاتورة ضريبية معتمدة")
    
    # حاوية الفاتورة (تصميم بسيط يشبه الصور السابقة)
    with st.container():
        st.info(f"**العميل:** {customer.name} | **المنتج:** {product.name} (x{qty})")
        st.write(f"**الإجمالي الأساسي:** {subtotal:,.2f} SAR")
        
        # حماية ضد الخطأ: نعرض النتيجة سواء كانت رقم أو نص من كودك
        if result is not None:
            st.success(f"**الصافي المطلوب (حسب النظام):** {result} SAR")
        else:
            st.warning("العملية تمت بنجاح (راجع التيرمنال للتفاصيل)")
            
    st.toast("تم تحديث المخزون وحساب الخصم بنجاح")
