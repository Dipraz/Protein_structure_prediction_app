#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio


# In[6]:


#st.set_page_config(layout = 'wide')
st.sidebar.markdown('''
    <h1 style="color: #4b0082 ; font-size: 36px; font-weight: bold; text-align: center; margin-bottom: 24px;">
        <span style="background-color: #48cae4; padding: 4px 12px; border-radius: 8px;">
            🧬 ESMFold
        </span>
    </h1>
    <h3 style="font-size: 24px; text-align: center; color: #000000;">
        End-to-End Structure Prediction with Deep Learning
    </h3>
''', unsafe_allow_html=True)


st.sidebar.write('[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

# In[25]:


# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon': {'color': 'spectrum'}, 'line': {'color': '#9fffcb', 'style': 'dash-dot', 'width': 1.0}})
    pdbview.setBackgroundColor('#e6e6fa')

    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height = 500,width=800)


# In[26]:


# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"

st.sidebar.markdown(
    """
    <style>
    .sidebar .stTextArea {
        background-color: #88ff00;
        color: #ff0088 ;
    }
    </style>
    """,
    unsafe_allow_html=True
)

txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)


# In[27]:


# ESMfold
def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    # Display protein structure
    st.subheader('Visualization of predicted protein structure')
    render_mol(pdb_string)

    # plDDT value is stored in the B-factor field
    st.subheader('plDDT(Predicted Local Distance Difference Test)')
    st.write('The plDDT score ranges from 0 to 100, where a higher score indicates a better prediction. ')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Download Protein Data Bank (PDB)",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )


# In[29]:


predict = st.sidebar.button('Predict', on_click=update)


# In[32]:


if not predict:
    st.warning('👈 Enter protein sequence data!')


# In[ ]:




