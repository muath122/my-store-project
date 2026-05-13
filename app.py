import streamlit as st
import Main  # استدعاء ملفك الأصلي كما هو

# إعدادات الصفحة
st.set_page_config(page_title="واجهة نظام المتجر", layout="wide")

# جلب البيانات من Main.py
products = Main.all_products
customers = Main.all_customers

st.title("🛍️ واجهة نظام المبيعات")

col1, col2 = st.columns(2)

with col1:
    st.header("إدخال الطلب")
    c_name = st.selectbox("اختر العميل", [c.name for c in customers])
    p_name = st.selectbox("اختر المنتج", [p.name for p in products])
    qty = st.number_input("الكمية", min_value=1, step=1)
    
    if st.button("تنفيذ العملية"):
        # جلب الكائنات (Objects) مباشرة
        customer = next(c for c in customers if c.name == c_name)
        product = next(p for p in products if p.name == p_name)
        
        # تنفيذ العمليات بنفس منطق التيرمنال
        subtotal = product.price * qty
        
        # استدعاء الدالة من كودك الأصلي (هي التي ستقرر الخصم والترقية)
        # نستخدم القيمة المرتجعة منها مباشرة للعرض
        final_price = customer.get_discount(subtotal)
        
        # تحديث المخزون باستخدام دالتك الأصلية
        product.update_stock(qty)
        
        with col2:
            st.header("المخرجات (مطابقة للتيرمنال)")
            st.success("تمت العملية بنجاح!")
            st.write(f"**العميل:** {customer.name} ({type(customer).__name__})")
            st.write(f"**المنتج:** {product.name}")
            st.write(f"**السعر الإجمالي:** {subtotal} SAR")
            
            # حساب الخصم فقط لأغراض العرض (الفرق بين الإجمالي وما أرجعته دالتك)
            actual_discount = subtotal - final_price
            st.write(f"**قيمة الخصم المطبق:** {actual_discount} SAR")
            
            st.divider()
            st.metric(label="المبلغ المطلوب دفعه", value=f"{final_price} SAR")

# تبويب جانبي لعرض المخزون (اختياري للتأكد من التحديث)
with st.sidebar:
    st.header("📦 حالة المخزون")
    for p in products:
        st.write(f"{p.name}: {p.stock}")
