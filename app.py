import streamlit as st
from supabase import create_client, Client
import uuid
import random
from datetime import datetime

url = st.secrets["url"]
key = st.secrets["key"]
supabase_client = create_client(url, key)

# # Configurar tu Supabase
# url = "https://xyzcompany.supabase.co"
# key = "your_supabase_api_key"
# supabase: Client = create_client(url, key)

def signup():
    st.sidebar.title("Registro")

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    yt_user = st.sidebar.text_input("YouTube User")
    user_id = st.sidebar.text_input("User ID")

    if st.sidebar.button("Registrar"):
        if email and password and yt_user and user_id:
            # Verificar si el usuario ya existe
            response = supabase_client.table('players').select('*').eq('email', email).execute()
            if response.data:
                st.sidebar.warning("El usuario ya está registrado.")
            else:
                # Registrar nuevo usuario
                supabase_client.table('players').insert({
                    "email": email,
                    "password": password,
                    "ytUser": yt_user,
                    "userId": user_id
                }).execute()
                st.sidebar.success("Registrado exitosamente.")
        else:
            st.sidebar.error("Por favor, completa todos los campos.")

def login():
    st.sidebar.title("Iniciar Sesión")

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Iniciar Sesión"):
        if email and password:
            response = supabase_client.table('players').select('*').eq('email', email).execute()
            if response.data:
                user = response.data[0]
                if user['password'] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.sidebar.success("Sesión iniciada.")
                else:
                    st.sidebar.error("Contraseña incorrecta.")
            else:
                st.sidebar.error("El email no está registrado.")
        else:
            st.sidebar.error("Por favor, ingresa email y contraseña.")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("Acceso")
    page = st.sidebar.radio("Selecciona una opción", ["Iniciar Sesión", "Registrarse"])

    if page == "Registrarse":
        signup()
    elif page == "Iniciar Sesión":
        login()
else:
    st.sidebar.write("Bienvenido,", st.session_state.user_email)
