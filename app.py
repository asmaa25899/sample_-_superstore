import streamlit as st
import pandas as pd
import bcrypt
import os

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="Power BI Login", page_icon="📊", layout="wide")

# ---------- إعداد مسار ملف المستخدمين ----------
FILE_PATH = "users.xlsx"

# ---------- بيانات المستخدم الافتراضي (اللي طلبتيها) ----------
DEFAULT_USER = {
    "username": "asmaa25899@gmail.com",
    "password": "asmaa25899"
}

# ---------- دالة لتشفير الباسورد (تُعيد سترينج) ----------
def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# ---------- إنشاء الملف وادخال المستخدم الافتراضي لو الملف مش موجود ----------
if not os.path.exists(FILE_PATH):
    # نجهّز داتا فريم بمستخدم افتراضي مشفّر
    hashed = hash_password(DEFAULT_USER["password"])
    df = pd.DataFrame({
        "username": [DEFAULT_USER["username"]],
        "password": [hashed]
    })
    df.to_excel(FILE_PATH, index=False)

# ---------- تحميل بيانات المستخدمين ----------
users_df = pd.read_excel(FILE_PATH)

# ---------- دالة حفظ المستخدمين إلى Excel ----------
def save_users(df):
    df.to_excel(FILE_PATH, index=False)

# ---------- دالة التحقق من المستخدم ----------
def verify_user(username, password):
    global users_df
    user = users_df[users_df["username"] == username]
    if not user.empty:
        # القيمة الموجودة في الملف عبارة عن سترينج تمثل ال-hash
        stored_hash = user["password"].values[0].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False

# ---------- دالة إضافة مستخدم جديد ----------
def add_user(username, password):
    global users_df
    hashed = hash_password(password)
    new_user = pd.DataFrame({"username": [username], "password": [hashed]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)

# ---------- حالة الجلسة ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- واجهة تسجيل الدخول ----------
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول إلى لوحة Power BI")

    option = st.sidebar.selectbox("اختر الإجراء", ["تسجيل الدخول", "إنشاء حساب جديد"])

    if option == "تسجيل الدخول":
        username = st.text_input("👤 اسم المستخدم أو الإيميل")
        password = st.text_input("🔑 كلمة المرور", type="password")
        if st.button("تسجيل الدخول"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ تم تسجيل الدخول بنجاح")
                st.experimental_rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

    elif option == "إنشاء حساب جديد":
        new_user = st.text_input("👤 اسم المستخدم الجديد (أو الإيميل)")
        new_pass = st.text_input("🔑 كلمة المرور الجديدة", type="password")
        if st.button("إنشاء الحساب"):
            if new_user in users_df["username"].values:
                st.error("⚠️ هذا الاسم مستخدم بالفعل. اختر اسمًا آخر.")
            else:
                add_user(new_user, new_pass)
                st.success("🎉 تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")

# ---------- واجهة Power BI بعد الدخول ----------
else:
    st.sidebar.success(f"مرحبًا {st.session_state.username} 👋")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    st.title("📊 Power BI Dashboard")

    st.markdown("""
    <div style="text-align:center; font-size:18px; margin-bottom:20px;">
        ✅ تم تسجيل الدخول بنجاح<br>
        يمكنك الآن استعراض لوحة التحكم الخاصة بك.
    </div>
    """, unsafe_allow_html=True)

    # 🔗 هنا ضعي رابط الـ Power BI بتاعك (استبدلي YOUR_LINK_HERE بالرابط الفعلي)
    # powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiYOUR_LINK_HERE..."

    # powerbi_url = "https://app.powerbi.com/groups/2635067f-8f70-46fe-a674-e7247b462fb2/reports/435fa762-fa3e-48e7-badd-4d1e48cba146/6f4a53caf8436a03514e?experience=power-bi"
    

powerbi_url =  "https://app.powerbi.com/groups/2635067f-8f70-46fe-a674-e7247b462fb2/dashboards/32d6b2e5-2dd5-4e89-af60-2fd4d3c01f0f?experience=power-bi&subfolderId=25289"

st.components.v1.iframe(powerbi_url, width=1200, height=700)
