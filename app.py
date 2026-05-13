import streamlit as st
import Main  # استدعاء ملف المنطق الأساسي
from datetime import datetime

# إعدادات النظام الرسمية
st.set_page_config(
    page_title="نظام إدارة المبيعات الموحد",
    page_icon="🖥️",
    layout="wide"
)

# تحسين المظهر العام باستخدام CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div.stButton > button:first-child {
        background-color: #004a99;
        color: white;
        border-radius: 5px;
        width: 100%;
        height: 3em;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #004a99;
        background-color: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# شريط المهام الجانبي
with st.sidebar:
    st.header("إدارة النظام")
    st.write(f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
    st.divider()
    st.caption("نظام إدارة مبيعات المتجر الإلكتروني - الإصدار 2.5")

# عنوان النظام الرسمي
st.title("🖥️ نظام إدارة العمليات والمبيعات")
st.write("منصة مركزية لإدارة سجلات العملاء، معالجة الطلبات الفورية، وتحديث المخزون.")

# جلب البيانات من ملف Main.py
products = Main.all_products
customers = Main.all_customers

# تقسيم الواجهة إلى تبويبات احترافية
tab_order, tab_stock = st.tabs(["🛒 معالجة طلب جديد", "📊 حالة المخزون"])

with tab_order:
    col_input, col_result = st.columns([1, 1], gap="large")
    
    with col_input:
        st.subheader("إدخال بيانات العملية")
        customer_name = st.selectbox("قاعدة بيانات العملاء", [c.name for c in customers], index=None, placeholder="اختر العميل...")
        product_name = st.selectbox("قائمة المنتجات المتاحة", [p.name for p in products], index=None, placeholder="اختر المنتج...")
        quantity = st.number_input("الكمية المطلوبة", min_value=1, step=1)
        
        submit_btn = st.button("اعتماد العملية وإصدار الفاتورة")

    with col_result:
        st.subheader("مخرجات النظام")
        if submit_btn:
            if not customer_name or not product_name:
                st.warning("يرجى تحديد العميل والمنتج لإتمام العملية.")
            else:
                customer = next(c for c in customers if c.name == customer_name)
                product = next(p for p in products if p.name == product_name)
                
                if quantity > product.stock:
                    st.error(f"فشل في إتمام العملية: المخزون الحالي ({product.stock}) أقل من الكمية المطلوبة.")
                else:
                    # حسابات الخصم والنهائي باستخدام منطق الكود الأصلي
                    subtotal = product.price * quantity
                    discount = customer.get_discount(subtotal)
                    final_amount = subtotal - discount
                    
                    # تحديث المخزون برمجياً
                    product.update_stock(quantity)
                    
                    # عرض النتائج في بطاقة رسمية
                    st.markdown(f"""
                    <div class="status-box">
                        <h4 style="color: #004a99;">✅ تم تأكيد العملية بنجاح</h4>
                        <hr>
                        <p><b>رقم المرجع:</b> {datetime.now().strftime('%H%M%S')}</p>
                        <p><b>المستفيد:</b> {customer.name}</p>
                        <p><b>البيان:</b> {product.name} (عدد {quantity})</p>
                        <p><b>إجمالي القيمة:</b> {subtotal:,.2f} SAR</p>
                        <p style="color: #d9534f;"><b>الخصم المطبق:</b> -{discount:,.2f} SAR</p>
                        <h3 style="color: #28a745;">صافي المستحق: {final_amount:,.2f} SAR</h3>
                    </div>
                    """, unsafe_allow_html=True)

with tab_stock:
    st.subheader("تقرير حالة المخزون الحالي")
    inventory_data = [{"المنتج": p.name, "السعر": f"{p.price:,.2f} SAR", "المخزون المتاح": p.stock} for p in products]
    st.table(inventory_data)
