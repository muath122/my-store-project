import streamlit as st
import Main  # الربط المباشر بالكود الأساسي

st.set_page_config(page_title="نظام المتجر", layout="centered")

# جلب القوائم من الكود الأساسي حقنا
products = Main.all_products
customers = Main.all_customers

st.title("🛍️ واجهة معالجة العمليات الموحدة")

# إدخال البيانات
c_name = st.selectbox("اختر العميل", [c.name for c in customers])
p_name = st.selectbox("اختر المنتج", [p.name for p in products])
qty = st.number_input("الكمية", min_value=1, step=1)

if st.button("تنفيذ العملية"):
    # تحديد الكائنات بناءً على الاختيار
    customer = next(c for c in customers if c.name == c_name)
    product = next(p for p in products if p.name == p_name)
    
    # الحساب الأساسي قبل الخصم
    subtotal = product.price * qty
    
    # القرار يأتي من الكود الأساسي فقط
    final_price = customer.get_discount(subtotal)
    
    # معالجة في حال كان الكود الأساسي يرجع None (بسبب الطباعة بدل الـ return)
    if final_price is None:
        # هنا الموقع سيطابق منطق التيرمنال تماماً في الحساب
        if "VIP" in type(customer).__name__:
            final_price = subtotal * 0.85 # خصم 15% للـ VIP
        else:
            final_price = subtotal * 0.95 # خصم 5% للعضو العادي

    # تنفيذ تحديث المخزون من الكود الأساسي
    product.update_stock(qty)
    
    # عرض المخرجات كما هي في التيرمنال
    st.divider()
    st.success("إتمام العملية بنجاح كما في النظام")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**العميل:** {customer.name} ({type(customer).__name__})")
        st.write(f"**المنتج:** {product.name}")
    with col2:
        st.write(f"**الإجمالي:** {subtotal:,.2f} SAR")
        st.write(f"**الخصم المطبق:** {subtotal - final_price:,.2f} SAR")
        
    st.subheader(f"الصافي المطلوب: {final_price:,.2f} SAR")
