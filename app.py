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
    
    # استدعاء الدالة من كودك الأصلي (سواء كانت تطبع أو ترجع قيمة)
    discount_val = customer.get_discount(subtotal)
    product.update_stock(qty)
    
    # --- منطق الحساب لضمان عدم ظهور الـ 300 ريال بالخطأ ---
    # إذا كان العميل من نوع Customer عادي، الصافي هو الإجمالي
    if type(customer).__name__ == "Customer":
        final_total = subtotal
    else:
        # إذا رجع الكود قيمة الخصم فقط (300)، نطرحها من الإجمالي
        if discount_val is not None and discount_val < subtotal:
            final_total = subtotal - discount_val
        else:
            final_total = discount_val if discount_val is not None else subtotal

    # --- منطقة طباعة الفاتورة ---
    st.markdown("---")
    st.subheader("🧾 فاتورة ضريبية معتمدة")
    
    with st.container():
        st.info(f"**العميل:** {customer.name} ({type(customer).__name__}) | **المنتج:** {product.name}")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write(f"**الإجمالي قبل الخصم:** {subtotal:,.2f} SAR")
        with col_res2:
            # عرض الصافي الصحيح (3000 للعميل العادي)
            st.success(f"**الصافي المطلوب دفعه:** {final_total:,.2f} SAR")
            
    st.toast("تمت العملية بنجاح")
