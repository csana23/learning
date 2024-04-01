from utils import enable_chat_history, display_msg
from streaming import StreamHandler
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from streaming import StreamHandler
# from langchain_core.callbacks import StreamingStdOutCallbackHandler

# from langchain.llms import OpenAI
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="Context aware chatbot", page_icon="⭐")
st.header('Context aware chatbot')
st.write('Enhancing Chatbot Interactions through Context Awareness')

class ContextChatbot:

    def __init__(self):
        self.model_id= "stabilityai/stablelm-3b-4e1t"
    
    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        # llm = OpenAI(model_name=_self.openai_model, temperature=0, streaming=True)
        tokenizer = AutoTokenizer.from_pretrained("stabilityai/stablelm-3b-4e1t")
        model = AutoModelForCausalLM.from_pretrained(
            "stabilityai/stablelm-3b-4e1t"
        )
        pipe = pipeline(
            "text-generation", 
            model=model, 
            tokenizer=tokenizer, 
            device=0, 
            max_new_tokens=20
        )
        hf = HuggingFacePipeline(pipeline=pipe)

        chain = ConversationChain(llm=hf, memory=memory, verbose=True)
        return chain
    
    @enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                response = chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()
