import streamlit as st
import Main  # الربط المباشر بملفك الأساسي

st.set_page_config(page_title="نظام المتجر", layout="centered")

# جلب البيانات من كودك الأساسي
products = Main.all_products
customers = Main.all_customers

st.title("🛍️ واجهة نظام المبيعات")

# مدخلات الواجهة فقط
c_name = st.selectbox("اختر العميل", [c.name for c in customers])
p_name = st.selectbox("اختر المنتج", [p.name for p in products])
qty = st.number_input("الكمية", min_value=1, step=1)

if st.button("تنفيذ العملية"):
    customer = next(c for c in customers if c.name == c_name)
    product = next(p for p in products if p.name == p_name)
    
    # حساب الإجمالي الأساسي (سعر المنتج * الكمية)
    subtotal = product.price * qty
    
    # الواجهة تطلب النتيجة من الكود الأساسي (القرار من الـ main)
    # ملاحظة: إذا ظهر لك خطأ هنا، فالمشكلة أن دالة get_discount تطبع ولا ترجع قيمة
    result = customer.get_discount(subtotal)
    
    # تحديث المخزون من دالتك الأصلية
    product.update_stock(qty)
    
    st.divider()
    
    # عرض النتائج المستلمة من الكود
    if result is not None:
        st.success(f"تمت العملية لـ {customer.name}")
        st.write(f"**الصافي المطلوب حسب النظام:** {result} SAR")
    else:
        # رسالة تنبيه إذا كانت الدالة في main تطبع فقط ولا ترجع قيمة
        st.error("نظام الحساب في الـ Main قام بالطباعة فقط ولم يرسل الرقم للواجهة.")
        st.info(f"الإجمالي قبل الخصم: {subtotal} SAR")
