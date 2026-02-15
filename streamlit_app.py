import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Bharat Biz-Agent",
    layout="wide"
)

st.title("🧠 Bharat Biz-Agent")
st.caption("Smart order & inventory assistant for small businesses")

if "http_session" not in st.session_state:
    st.session_state.http_session = requests.Session()


# ---------------- SESSION STATE INIT ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------------- SIDEBAR ----------------
st.sidebar.title("Mode")
mode = st.sidebar.radio("Select role", ["Customer", "Admin"])

# ---------------- SAFE MODE SWITCH RESET ----------------
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

if st.session_state.current_mode != mode:
    st.session_state.current_mode = mode

    # Reset admin login if switching back to Customer
    if mode == "Customer":
        st.session_state.admin_logged_in = False


# =================================================
# 👤 CUSTOMER MODE
# =================================================
if mode == "Customer":
    st.subheader("💬 AI Order Assistant")
    st.caption("Talk naturally, just like WhatsApp")

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"🧑 **Customer:** {msg}")
        else:
            st.markdown(f"🤖 **Assistant:** {msg}")

    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_input(
            "Type a message",
            placeholder="bhai kya milega"
        )
        send = st.form_submit_button("Send")

    if send and user_message.strip():
        st.session_state.chat_history.append(("user", user_message))

        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[-20:]


        with st.spinner("Assistant is thinking..."):
            try:
                res = st.session_state.http_session.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": user_message},
                    timeout=5
                )
                response = res.json()
            except Exception:
                response = {"assistant": "Server is currently unavailable."}

        if "assistant" in response:
            st.session_state.chat_history.append(
                ("assistant", response["assistant"])
            )

            if len(st.session_state.chat_history) > 20:
                st.session_state.chat_history = st.session_state.chat_history[-20:]
        else:
            if "assistant" in response:
                st.session_state.chat_history.append(
                    ("assistant", response["assistant"])
                )
                if len(st.session_state.chat_history) > 20:
                    st.session_state.chat_history = st.session_state.chat_history[-20:]

            elif "item" in response:
                st.session_state.chat_history.append(
                    (
                        "assistant",
                        f"Order confirmed ✅\n"
                        f"{response['item']} x {response['quantity']} = ₹{response['total']}"
                    )
                )
            elif "error" in response:
                st.session_state.chat_history.append(
                    (
                        "assistant",
                        f"Order rejected ❌\n"
                        f"Available quantity: {response.get('available_quantity', 0)}"
                    )
                )

# =================================================
# 🧑‍💼 ADMIN MODE
# =================================================
elif mode == "Admin":

    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"

    st.subheader("🔐 Admin Login")

    # -------- NOT LOGGED IN --------
    if not st.session_state.admin_logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == ADMIN_USER and password == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.success("Admin access granted")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # -------- LOGGED IN --------
    else:
        st.success("Admin access granted")

        st.markdown("### 💰 Revenue Overview")

        rev_res = requests.get(f"{BACKEND_URL}/revenue")
        rev_data = rev_res.json()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Revenue", f"₹{rev_data['total_revenue']}")

        with col2:
            st.metric("Today's Revenue", f"₹{rev_data['today_revenue']}")


        st.markdown("### 📦 Inventory")

        res = requests.get(f"{BACKEND_URL}/inventory")
        inventory = res.json()["inventory"]

        for item in inventory:
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.text(item["name"])

            with col2:
                qty = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=item["quantity"],
                    key=f"qty_{item['id']}"
                )

            with col3:
                if st.button("Update", key=f"update_{item['id']}"):
                    requests.post(
                        f"{BACKEND_URL}/update_inventory",
                        json={
                            "id": item["id"],
                            "quantity": qty
                        }
                    )
                    st.success(f"{item['name']} updated")

        st.markdown("### 📊 Stock Overview")

        stock_res = requests.get(f"{BACKEND_URL}/inventory")
        stock_data = stock_res.json()["inventory"]

        stock_table = []

        for item in stock_data:
            stock_table.append({
                "Item": item["name"],
                "Quantity": item["quantity"],
                "Price (₹)": item["price"],
                "Status": "Low Stock ⚠️" if item["quantity"] <= 2 else "In Stock ✅"
            })

        st.dataframe(stock_table, use_container_width=True)




        st.markdown("### 📑 Orders")
        res = requests.get(f"{BACKEND_URL}/orders")
        st.table(res.json()["orders"])

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()



        
