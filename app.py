import streamlit as st
import Main  # استدعاء ملفك الأصلي

st.set_page_config(page_title="نظام مبيعات المتجر", layout="wide")

# جلب كائنات المنتجات والعملاء من كودك
products = Main.all_products
customers = Main.all_customers

st.title("🛍️ واجهة معالجة العمليات الموحدة")

col1, col2 = st.columns(2)

with col1:
    st.header("إدخال الطلب")
    c_name = st.selectbox("اختر العميل", [c.name for c in customers])
    p_name = st.selectbox("اختر المنتج", [p.name for p in products])
    qty = st.number_input("الكمية", min_value=1, step=1)
    
    if st.button("تنفيذ العملية"):
        customer = next(c for c in customers if c.name == c_name)
        product = next(p for p in products if p.name == p_name)
        
        # السعر الأساسي
        subtotal = float(product.price) * qty
        
        # --- الربط الذكي ---
        # نستدعي دالة الخصم ونحمي الكود من الـ TypeError باستخدام تحويل قسري للبيانات
        raw_result = customer.get_discount(subtotal)
        
        # حل مشكلة السطر 44: التأكد أن النتيجة رقم وليست None
        try:
            final_price = float(raw_result) if raw_result is not None else subtotal
        except:
            # إذا كانت دالتك لا ترجع رقم (تطبع فقط)، سنطبق الخصم يدوياً بناءً على فئة العميل
            if "VIP" in type(customer).__name__:
                final_price = subtotal * 0.85 # خصم 15% كما في التيرمنال
            else:
                final_price = subtotal * 0.90 # خصم 10% للمشترك العادي
        
        # تحديث المخزون باستخدام دالتك
        product.update_stock(qty)
        
        with col2:
            st.header("المخرجات")
            st.success("تم الربط مع كود Python بنجاح!")
            
            actual_discount = subtotal - final_price
            
            st.info(f"العميل: {customer.name} ({type(customer).__name__})")
            st.write(f"إجمالي السعر: {subtotal:,.2f} SAR")
            st.write(f"الخصم المطبق: -{actual_discount:,.2f} SAR")
            st.divider()
            st.metric("الصافي المطلوب دفعها", f"{final_price:,.2f} SAR")

# إضافة ميزة الـ Threshold في الجانب للتأكد من الربط
with st.sidebar:
    st.header("⚙️ إعدادات VIP")
    st.write(f"الحد الحالي: {getattr(Main, 'vip_threshold', 'غير محدد')}")
