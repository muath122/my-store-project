import streamlit as st
import Main  # استدعاء ملفك الأصلي
from datetime import datetime

# إعدادات النظام الرسمية
st.set_page_config(
    page_title="نظام إدارة المبيعات الموحد",
    page_icon="🖥️",
    layout="wide"
)

# تصميم الواجهة (Dashboard CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    div.stButton > button:first-child {
        background-color: #002b5c;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
    }
    .invoice-card {
        padding: 25px;
        border-radius: 12px;
        border-right: 8px solid #002b5c;
        background-color: #ffffff;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2502/2502127.png", width=80)
    st.header("إدارة النظام")
    st.info(f"📅 تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
    st.divider()
    st.caption("نظام تخطيط موارد المؤسسات (ERP) - الإصدار 2.5")

# العنوان الرئيسي
st.title("🖥️ مركز معالجة العمليات والمبيعات")

# جلب البيانات
try:
    products = Main.all_products
    customers = Main.all_customers
except AttributeError:
    st.error("خطأ: يرجى التأكد من تعريف all_products و all_customers في ملف Main.py")
    st.stop()

# التبويبات
tab_order, tab_admin = st.tabs(["🛒 معالجة طلب جديد", "📊 السجلات والمخزون"])

with tab_order:
    col_input, col_result = st.columns([1, 1], gap="large")
    
    with col_input:
        st.subheader("إدخال بيانات العملية")
        customer_name = st.selectbox("قاعدة بيانات العملاء", [c.name for c in customers], index=None, placeholder="ابحث عن العميل...")
        product_name = st.selectbox("دليل المنتجات المتاحة", [p.name for p in products], index=None, placeholder="ابحث عن المنتج...")
        quantity = st.number_input("الكمية المطلوبة", min_value=1, step=1)
        
        submit_btn = st.button("تأكيد العملية وإصدار الفاتورة")

    with col_result:
        st.subheader("معاينة الفاتورة")
        if submit_btn:
            if not customer_name or not product_name:
                st.warning("يرجى تحديد العميل والمنتج.")
            else:
                customer = next(c for c in customers if c.name == customer_name)
                product = next(p for p in products if p.name == product_name)
                
                if quantity > product.stock:
                    st.error(f"فشل المعالجة: المخزون الحالي ({product.stock}) غير كافٍ.")
                else:
                    # حساب المالية مع تفعيل منطق الخصم من كودك
                    subtotal = float(product.price) * quantity
                    
                    # استدعاء دالة الخصم والتأكد من أنها تعيد رقماً
                    discount = customer.get_discount(subtotal)
                    # معالجة في حال كانت الدالة تعيد السعر بعد الخصم بدلاً من قيمة الخصم نفسه
                    if discount > subtotal: 
                        final_amount = float(discount)
                        discount_value = subtotal - final_amount
                    else:
                        discount_value = float(discount)
                        final_amount = subtotal - discount_value
                    
                    product.update_stock(quantity)
                    
                    st.balloons()
                    st.markdown(f"""
                    <div class="invoice-card">
                        <h4 style="color: #002b5c;">🧾 فاتورة ضريبية معتمدة</h4>
                        <hr>
                        <p><b>رقم العملية:</b> {datetime.now().strftime('%Y%H%M%S')}</p>
                        <p><b>العميل:</b> {customer.name} (<span style="color: #002b5c;">{type(customer).__name__}</span>)</p>
                        <p><b>البيان:</b> {product.name} (عدد {quantity})</p>
                        <p style="font-size: 1.1em;">إجمالي القيمة: <b>{subtotal:,.2f} SAR</b></p>
                        <p style="color: #d9534f; font-size: 1.1em;">الخصم المطبق: <b>-{discount_value:,.2f} SAR</b></p>
                        <h2 style="color: #28a745; margin-top: 10px;">صافي المستحق: {final_amount:,.2f} SAR</h2>
                    </div>
                    """, unsafe_allow_html=True)

with tab_admin:
    col_inv, col_cust = st.columns(2)
    
    with col_inv:
        st.subheader("📊 مراقبة المخزون")
        inv_data = [{"المنتج": p.name, "السعر": f"{p.price} SAR", "المخزون": p.stock} for p in products]
        st.table(inv_data)
        
    with col_cust:
        st.subheader("👥 سجل العملاء")
        # عرض نوع العميل (Member/VIP/Customer) بناءً على الكلاس الخاص به في كودك
        cust_data = [{"العميل": c.name, "الفئة": type(c).__name__} for c in customers]
        st.table(cust_data)
