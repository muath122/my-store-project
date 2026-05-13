import streamlit as st
import Main  # استدعاء ملفك الأصلي
from datetime import datetime

# إعدادات النظام الرسمية
st.set_page_config(
    page_title="نظام إدارة المبيعات الموحد",
    page_icon="🖥️",
    layout="wide"
)

# تحسين المظهر العام باستخدام CSS لجعلها واجهة "Dashboard" فخمة
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
        border: none;
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

# شريط المهام الجانبي الإداري
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2502/2502127.png", width=80)
    st.header("إدارة النظام")
    st.info(f"📅 تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
    st.divider()
    st.caption("نظام تخطيط موارد المؤسسات (ERP) - الإصدار 2.5")

# العنوان الرئيسي
st.title("🖥️ مركز معالجة العمليات والمبيعات")
st.write("منصة مركزية لإدارة العمليات التجارية وحساب الاستحقاقات المالية بدقة.")

# جلب البيانات من ملف Main.py (مع التأكد من وجودها)
try:
    products = Main.all_products
    customers = Main.all_customers
except AttributeError:
    st.error("خطأ في ربط البيانات: يرجى التأكد من تعريف القوائم في ملف Main.py")
    st.stop()

# تقسيم الواجهة إلى تبويبات احترافية
tab_order, tab_stock = st.tabs(["🛒 معالجة طلب جديد", "📊 مراقبة المخزون"])

with tab_order:
    col_input, col_result = st.columns([1, 1], gap="large")
    
    with col_input:
        st.subheader("إدخال بيانات العملية")
        customer_name = st.selectbox("قاعدة بيانات العملاء", [c.name for c in customers], index=None, placeholder="ابحث عن العميل...")
        product_name = st.selectbox("دليل المنتجات المتاحة", [p.name for p in products], index=None, placeholder="ابحث عن المنتج...")
        quantity = st.number_input("الكمية المطلوبة (وحدات)", min_value=1, step=1)
        
        submit_btn = st.button("تأكيد العملية وإصدار الفاتورة")

    with col_result:
        st.subheader("معاينة الفاتورة")
        if submit_btn:
            if not customer_name or not product_name:
                st.warning("يرجى تحديد العميل والمنتج لإتمام العملية.")
            else:
                customer = next(c for c in customers if c.name == customer_name)
                product = next(p for p in products if p.name == product_name)
                
                if quantity > product.stock:
                    st.error(f"فشل المعالجة: المخزون الحالي ({product.stock}) أقل من الكمية المطلوبة.")
                else:
                    try:
                        # الحسابات المالية
                        subtotal = float(product.price) * quantity
                        
                        # الحصول على الخصم (تحويله لرقم لضمان عدم حدوث TypeError)
                        discount_raw = customer.get_discount(subtotal)
                        discount = float(discount_raw) if isinstance(discount_raw, (int, float)) else 0.0
                        
                        final_amount = subtotal - discount
                        
                        # تحديث المخزون
                        product.update_stock(quantity)
                        
                        # عرض الفاتورة الرسمية
                        st.balloons()
                        st.markdown(f"""
                        <div class="invoice-card">
                            <h4 style="color: #002b5c;">🧾 فاتورة ضريبية معتمدة</h4>
                            <hr>
                            <p><b>رقم العملية:</b> {datetime.now().strftime('%Y%H%M%S')}</p>
                            <p><b>العميل المستفيد:</b> {customer.name}</p>
                            <p><b>تفاصيل البيان:</b> {product.name} (عدد {quantity})</p>
                            <p style="font-size: 1.1em;">إجمالي القيمة: <b>{subtotal:,.2f} SAR</b></p>
                            <p style="color: #d9534f; font-size: 1.1em;">الخصم المطبق: <b>-{discount:,.2f} SAR</b></p>
                            <h2 style="color: #28a745; margin-top: 10px;">صافي المستحق: {final_amount:,.2f} SAR</h2>
                            <p style="font-size: 0.8em; color: gray;">تمت المعالجة آلياً بتاريخ {datetime.now().strftime('%H:%M:%S')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"خطأ في العمليات الحسابية: تأكد من أن دالة الخصم تعيد أرقاماً فقط.")

with tab_stock:
    st.subheader("تقرير حالة المخزون اللحظي")
    inventory_data = [{"المنتج": p.name, "سعر الوحدة": f"{p.price:,.2f} SAR", "المخزون المتبقي": p.stock} for p in products]
    st.table(inventory_data)
