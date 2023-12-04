import asyncio
import streamlit as st
import os
from httpx_oauth.clients.google import GoogleOAuth2

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
REDIRECT_URI = "https://hukusyuoapp-jb3msdbvcgjeghpjaa6wys.streamlit.app/"

async def write_authorization_url(client):
    authorization_url = await client.get_authorization_url(
        REDIRECT_URI,
        scope=["profile", "email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url

async def write_access_token(client, code):
    token = await client.get_access_token(code, REDIRECT_URI)
    return token

async def get_email(client, token):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email

def google_oauth2_required(func):
    def wrapper(*args, **kwargs):
        client = GoogleOAuth2(client_id, client_secret)
        authorization_url = asyncio.run(write_authorization_url(client))

        if "token" not in st.session_state:
            st.session_state.token = None

        if st.session_state.token is None:
            try:
                code = st.experimental_get_query_params()["code"]
            except KeyError:
                st.write(
                    f"""<h1>
                    Please login using this <a target="_self"
                    href="{authorization_url}">url</a></h1>""",
                    unsafe_allow_html=True,
                )
                return
            token = asyncio.run(write_access_token(client, code))
            if token is None:
                st.write("Error in getting the access token.")
                return
            st.session_state["token"] = token
            user_id, user_email = asyncio.run(get_email(client, token["access_token"]))
            st.session_state.user_id = user_id
            st.session_state.user_email = user_email

        func(*args, **kwargs)

    return wrapper