import streamlit as st

from agent.react_agent import ReactAgent

st.title("RoboCare智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    res_message = []
    with st.spinner("思考中……"):
        res = st.session_state["agent"].execute_stream(prompt)


        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(capture(res, res_message))
        st.session_state["messages"].append({"role": "assistant", "content": res_message[-1]})
        st.rerun()
