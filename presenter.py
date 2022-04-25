import streamlit as st
import view

pview = view.View()

st.title('MLiP HW3 Part3 - Chunying Li')

st.image("image/MLiP - HW3 - part2.png")

# Input the probability
pview.p_botrytis = st.number_input('Input chance of botrytis', min_value=0.0, max_value=1.0, value=0.1, on_change=pview.calculate_e_value())
pview.p_no_sugar = st.number_input('Input chance of no sugar level', min_value=0.0, max_value=1.0, value=0.6, on_change=pview.calculate_e_value())
pview.p_typical_sugar = st.number_input('Input chance of typical sugar level', min_value=0.0, max_value=1.0, value=0.3, on_change=pview.calculate_e_value())
pview.p_high_sugar = st.number_input('Input chance of high sugar level', min_value=0.0, max_value=1.0, value=0.1, on_change=pview.calculate_e_value())

# Display the value
st.subheader('E-value')
st.write(pview.e_value)

# Display the alternative
st.subheader('Recommended alternative')
st.write(pview.alternative)


