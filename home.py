import streamlit as st
from savingsAccount import SavingsAccount
from currentAccount import CurrentAccount

st.set_page_config(page_title="OMEGA Bank App", layout="centered")

USERS = {
    "sulesaada19@gmail.com": {"password": "1234", "savings": 200000, "current": 50000},
    "calebonuh@gmail.com": {"password": "@123", "savings": 40000, "current": 1000000},
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

st.title("OMEGA Bank App")
st.header("Hi, welcome to OMEGA Bank App")
st.write("Your one-stop solution for digital banking.")
st.subheader("I AM SAADA, YOUR DIGITAL BANKING ASSISTANT")
st.balloons()

# Login Section
if not st.session_state.logged_in:
    st.subheader("Login")
    useremail = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if useremail in USERS and USERS[useremail]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = useremail
            st.session_state.account_data = USERS[useremail]
            st.success(f"Welcome back, {useremail}!")
        else:
            st.error("Invalid email or password.")

# If Logged In
if st.session_state.logged_in:
    user_data = st.session_state.get("account_data")

    if user_data:
        savingsAccount = SavingsAccount(user_data["savings"])
        currentAccount = CurrentAccount(user_data["current"])

        st.subheader("Choose Account Type")
        account_type = st.radio("Select an account:", ["Savings Account", "Current Account"])

        st.subheader("Transaction Options")
        transaction_type = st.selectbox("Select a transaction:", ["Deposit", "Withdraw", "Check Balance"])
        amount = st.number_input("Enter amount:", min_value=0.0, max_value=500000.0)

        if st.button("Submit"):
            if account_type == "Savings Account":
                if transaction_type == "Deposit":
                    if amount > 0:
                        savingsAccount.deposit(amount)
                        user_data["savings"] = savingsAccount.balance
                        st.success(f"Successfully deposited N{amount:.2f} into Savings Account.")
                    else:
                        st.error("Deposit amount must be greater than zero.")

                elif transaction_type == "Withdraw":
                    if amount > 0:
                        if savingsAccount.withdraw(amount):
                            user_data["savings"] = savingsAccount.balance
                            st.success(f"Successfully withdrew N{amount:.2f} from Savings Account.")
                        else:
                            st.error("Insufficient funds in Savings Account.")
                    else:
                        st.error("Withdrawal amount must be greater than zero.")

                elif transaction_type == "Check Balance":
                    st.info(f"Savings Balance: N{savingsAccount.balance:.2f}")

            elif account_type == "Current Account":
                if transaction_type == "Deposit":
                    if amount > 0:
                        currentAccount.deposit(amount)
                        user_data["current"] = currentAccount.balance
                        st.success(f"Successfully deposited N{amount:.2f} into Current Account.")
                    else:
                        st.error("Deposit amount must be greater than zero.")

                elif transaction_type == "Withdraw":
                    if amount > 0:
                        if currentAccount.withdraw(amount):
                            user_data["current"] = currentAccount.balance
                            st.success(f"Successfully withdrew N{amount:.2f} from Current Account.")
                        else:
                            st.error("Insufficient funds in Current Account.")
                    else:
                        st.error("Withdrawal amount must be greater than zero.")

                elif transaction_type == "Check Balance":
                    st.info(f"Current Balance: N{currentAccount.balance:.2f}")

        if st.button("Logout"):
            st.session_state.update(logged_in=False, user=None, account_data=None)
            st.success("You have been logged out.")