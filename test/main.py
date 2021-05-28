import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title("Streamlit Test")

"Start!!!"
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Iteration {i+1}")
    bar.progress(i + 1)
    time.sleep(0.01)
"Done!!"

# left_column, right_column = st.beta_columns(2)
# button = left_column.button("display in left_column")
# if button:
#     right_column.write("right_column here")

expander = st.beta_expander("Inquiry")
expander.write("write")

text = st.text_input("What's your hobby？",value="hobby")
"Your hobby:",text

option = st.selectbox(
    "What's your favorite number？",
    list(range(1,11)),
)
"Your favorite number:", option

condition = st.slider("How's your condition？", 0, 100, 50)
"Your condition:", condition

if st.checkbox("Show Image"):
    img = Image.open('Python1.png')
    st.image(img, caption="Python", use_column_width=True)

