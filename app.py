import streamlit as st
import pandas as pd
from data import read_file, get_content_text
from RAG import QueryHandler

# Load data from Excel
file_path = r'Sales_Sol_Sheet.csv'
df = read_file(file_path)


# Initialize QueryHandler
query_handler = QueryHandler()

# Page title
st.title("Email Generator")

# Section for recipient details (presets)
st.header("Enter Recipient Details")

# Initialize recipient and sender details in session state if not already present
if 'presets' not in st.session_state:
    st.session_state.presets = {
        'Recipient': "Adam Smith",
        'Recipient_Designation': "CFO",
        'Recipient_Function': "Finance",
        'Recipient_Company': "John Deere",
        'Website': "https://www.example.com"
    }

if 'context' not in st.session_state:
    st.session_state.context = {
        'Sender_Company': "Diacto Technologies",
        'Sender_Name': "John Doe",
        'Sender_Designation': "Sales Manager",
        'Sender_summary': '''Diacto is a global consulting firm specializing in Business Intelligence (BI), Data Engineering, and Artificial Intelligence (AI) services.
                             They assist organizations in transforming extensive data from various sources into actionable insights, enhancing operational efficiency and driving growth.
                             With over 600 successful BI implementations worldwide, Diacto offers end-to-end services, including data strategy, engineering, analytics, and visualization.
                             Their team of certified consultants is dedicated to delivering high-quality solutions tailored to client needs.''',
        'case_studies': [],
        'dashboards': [],
        'Rec_summary': 'No description available',
        'Industry': 'No industry information available',
        'clients': 'Emerson, Barry Wehmiller, Elkay Silicones, Afnitas, Alleima, Trimble'
    }

# Update session state based on user input
st.session_state.presets['Recipient'] = st.text_input("Recipient Name", st.session_state.presets['Recipient'])
st.session_state.presets['Recipient_Designation'] = st.text_input("Recipient Designation", st.session_state.presets['Recipient_Designation'])
st.session_state.presets['Recipient_Function'] = st.text_input("Recipient Function", st.session_state.presets['Recipient_Function'])
st.session_state.presets['Recipient_Company'] = st.text_input("Recipient Company", st.session_state.presets['Recipient_Company'])
st.session_state.presets['Website'] = st.text_input("Website", st.session_state.presets['Website'])

# Section for sender context
st.header("Enter Sender Details")
st.session_state.context['Sender_Company'] = st.text_input("Sender Company", st.session_state.context['Sender_Company'])
st.session_state.context['Sender_Name'] = st.text_input("Sender Name", st.session_state.context['Sender_Name'])
st.session_state.context['Sender_Designation'] = st.text_input("Sender Designation", st.session_state.context['Sender_Designation'])
st.session_state.context['Sender_summary'] = st.text_area("Sender Summary", st.session_state.context['Sender_summary'])

# Button to fetch data from the database and process content
def update_context(context, presets, query_handler, df):
    summary_data = None
  # Button to fetch data from the database and process content
  try:
      # Fetch content text from URL
      url = st.session_state.presets['Website']
      content_text = get_content_text(url)
      summary_data = query_handler.summarize_page(content_text)

      # Check if parsing was successful and update session state context
      if isinstance(summary_data, dict):
          # Update context with Industry and Description
          st.session_state.context.update({
              'Rec_summary': summary_data.get('Description', 'No description available'),
              'Industry': summary_data.get('Industry', 'No industry information available')
          })

          # Filter DataFrame by Industry and Function
          filtered_df = df[(df['Industry'] == context['Industry']) &
                          (df['Function'] == presets['Recipient_Function'])]


          # Create case_studies list
          case_studies = {}
          for _, row in filtered_df.iterrows():
              if pd.notna(row['Casestudy one liners']):
                case_studies.update({"name":row['Casestudy Title'] , "summary": row['Casestudy one liners'], "link": f'{row["Case Study Link"]}'})
          # Create dashboards list
          dashboards = {}
          for _, row in filtered_df.iterrows():
              if pd.notna(row['Dashboard Title']) or pd.notna(row['Dashboard Description']):
                  dashboards.update({"name": row['Dashboard Title'], "summary": row['Dashboard Description'], "link": row['Dashboard Link']})
                  

          clients = filtered_df['Clients Served'].dropna().unique().tolist()
          clients = ', '.join(clients) if clients else None


          # Update context with fetched case studies and dashboards
          st.session_state.context.update({
              'case_studies': case_studies,
              'dashboards': dashboards,
              'clients' : clients
          })

          print("Data fetched and processed successfully")
  except Exception as e:
      print(f"Error: {e}")
      print(summary_data)
      print("Failed to fetch or parse data")



update_context(st.session_state.context, st.session_state.presets, query_handler, df)

# Button to generate email
if st.button("Generate Email"):
    # Generate email content based on session state presets and context
    generated_email = query_handler.generate_email(st.session_state.presets, st.session_state.context, print_context=True)
    st.subheader("Generated Email")
    #st.write(generated_email)
    st.markdown(f"<div style='word-wrap: break-word;'>{generated_email}</div>", unsafe_allow_html=True)
