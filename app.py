import streamlit as st
import Main # كودك الأصلي

st.set_page_config(page_title="Electronic Store System", layout="centered")

st.title("🛒 نظام مبيعات المتجر الإلكتروني")
st.write("مرحباً دكتور، هذا النظام مربوط بكود البايثون الأساسي.")

# قراءة البيانات من كودك
products = Main.all_products
customers = Main.all_customers

# واجهة الموقع
col1, col2 = st.columns(2)

with col1:
    c_name = st.selectbox("اختر العميل", [c.name for c in customers])
with col2:
    p_name = st.selectbox("اختر المنتج", [p.name for p in products])

qty = st.number_input("الكمية", min_value=1, value=1)

if st.button("إتمام العملية وحساب الخصم"):
    customer = next(c for c in customers if c.name == c_name)
    product = next(p for p in products if p.name == p_name)
    
    if qty > product.stock:
        st.error(f"المخزون لا يكفي! المتوفر {product.stock} فقط.")
    else:
        subtotal = product.price * qty
        # استخدام دالة الخصم من كودك
        discount = customer.get_discount(subtotal)
        final = subtotal - discount
        
        st.balloons() # تأثير احتفالي عند النجاح
        st.success(f"تمت العملية بنجاح!")
        st.write(f"**العميل:** {customer.name}")
        st.write(f"**المجموع قبل الخصم:** {subtotal:.2f} SAR")
        st.write(f"**قيمة الخصم:** {discount:.2f} SAR")
        st.header(f"المبلغ المطلوب: {final:.2f} SAR")