import streamlit as st
import streamlit.components.v1 as components
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Remove these lines as we no longer need them
# import os
# from dotenv import load_dotenv
# load_dotenv()

# Set up the page configuration
st.set_page_config(page_title="p5.js Sketch Generator", layout="wide")

# Move the LLM initialization inside the main function
# Remove the global LLM initialization

def generate_p5js_sketch(action, api_key):
    try:
        llm = ChatOpenAI(temperature=0.7, api_key=api_key)
        prompt = ChatPromptTemplate.from_template(
            "Generate a basic p5.js sketch that {action}. Provide only the code without any explanations, annotations, or markdown formatting. Do not include ```javascript tags or any other non-code elements."
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(action=action)
        return result.strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("p5.js Sketch Generator")

    # User input for the OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    # User input for the sketch action
    action = st.text_input("Enter the action for p5.js sketch:", "creates a simple animation")

    # Generate button
    if st.button("Generate Sketch"):
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            with st.spinner("Generating p5.js sketch..."):
                p5js_code = generate_p5js_sketch(action, api_key)
            
            if p5js_code:
                # Display the generated code
                st.subheader("Generated p5.js Code:")
                st.code(p5js_code, language="javascript")

                # Create and display the p5.js sketch
                sketch_html = f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
                <script>
                {p5js_code}
                </script>
                <div id="sketch-holder"></div>
                """
                st.subheader("Rendered p5.js Sketch:")
                components.html(sketch_html, height=450)

if __name__ == "__main__":
    main()
