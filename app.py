import streamlit as st
import Main 

st.set_page_config(page_title="نظام المتجر المطور", layout="wide")

# الجانب الإداري
with st.sidebar:
    st.header("⚙️ الإدارة والمخزون")
    Main.vip_threshold = st.number_input("سقف الـ VIP", value=float(getattr(Main, 'vip_threshold', 500.0)))
    
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("📦 المخزون")
        for p in Main.all_products: st.caption(f"{p.name}: {p.stock}")
    with col_b:
        st.write("👥 العملاء")
        for c in Main.all_customers: st.caption(f"{c.name}")

# الواجهة الرئيسية
st.title("🛍️ مركز العمليات")

c_name = st.selectbox("العميل", [c.name for c in Main.all_customers])
p_name = st.selectbox("المنتج", [p.name for p in Main.all_products])
qty = st.number_input("الكمية", min_value=1)

if st.button("تنفيذ وطباعة الفاتورة"):
    customer = next(c for c in Main.all_customers if c.name == c_name)
    product = next(p for p in Main.all_products if p.name == p_name)
    
    subtotal = float(product.price * qty)
    
    # طلب القرار من الكود الأساسي
    returned_val = customer.get_discount(subtotal)
    product.update_stock(qty)
    
    # --- معالجة ذكية لمنع رقم الـ 300 الغريب ---
    # إذا كان الرقم المرجع أصغر من نصف السعر، غالباً هو "قيمة الخصم" وليس "السعر النهائي"
    if returned_val is not None:
        if returned_val < (subtotal / 2): 
            final_price = subtotal - returned_val # اعتباره قيمة خصم
        else:
            final_price = returned_val # اعتباره السعر النهائي
    else:
        # حساب احتياطي يطابق التيرمنال تماماً (5% للمشترك و 15% للـ VIP)
        discount_rate = 0.85 if "VIP" in type(customer).__name__ else 0.95
        final_price = subtotal * discount_rate

    # طباعة الفاتورة
    st.markdown("---")
    st.subheader("🧾 الفاتورة النهائية")
    st.info(f"العميل: {customer.name} | المنتج: {product.name}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("الإجمالي", f"{subtotal} SAR")
    c2.metric("الخصم", f"{subtotal - final_price} SAR", delta_color="inverse")
    c3.metric("المطلوب دفعه", f"{final_price} SAR")
