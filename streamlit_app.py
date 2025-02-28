import streamlit as st
from Agents.MainAgent import MainAgent  # Ensure this import works properly

# Initialize the MainAgent
agent = MainAgent()

# Streamlit UI with dark mode settings
# st.set_page_config(page_title="BNPL", layout="centered")

# # Apply custom CSS to center and enlarge the title
# st.markdown(
#     """
#     <style>
#         .title {
#             text-align: center;
#             font-size: 1000px;
#             font-weight: bold;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Display the title
# st.markdown('<h1 class="title">BNPL</h1>', unsafe_allow_html=True)
st.image("freepik__a-clean-corporate-background-with-fiza-financial-i__27235.png", width=1500)

# Center align the button
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
if st.button("Generate Plan"):
    try:
        # Prepare the input data dictionary
        input_data = {
            "club_name": "El Ahly Club",
            "car_name": "Suzuki",
            "car_model": "Swift",
            "uni_name": "Ain Shams",
            "college_name": "Computer Science",
            "client_name": 7,
        }
        
        # Agent configuration
        config = {"configurable": {"thread_id": 1}}
        
        # Run the agent and fetch results
        result = agent.graph.invoke(input_data, config=config)
        
        # Extract and display suggestions
        if "suggestions" in result:
            suggestions = result["suggestions"].content
            st.subheader("FIZA Plan Suggestions:")
            st.markdown(suggestions)
        else:
            st.error("No suggestions found in the response.")
    except ValueError:
        st.error("Client ID must be a valid number!")
    except Exception as e:
        st.error(f"Error: {str(e)}")
st.markdown("</div>", unsafe_allow_html=True)
