import streamlit as st
from Agents.MainAgent import MainAgent  # Ensure this import works properly

# Initialize the MainAgent
agent = MainAgent()

# Streamlit UI with dark mode settings
st.set_page_config(page_title="Google AI Finance Hackathon - BNPL", layout="centered")

# Streamlit default dark mode (works with Streamlit themes)
st.title("Google AI Finance Hackathon - BNPL")
st.image("R.jpg", width=850)

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
            st.subheader("BNPL Plan Suggestions:")
            st.markdown(suggestions)
        else:
            st.error("No suggestions found in the response.")
    except ValueError:
        st.error("Client ID must be a valid number!")
    except Exception as e:
        st.error(f"Error: {str(e)}")
st.markdown("</div>", unsafe_allow_html=True)
