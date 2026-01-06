import streamlit as st
import pandas as pd

# Load data from Excel
@st.cache_data
def load_data():
    df = pd.read_excel("career_recommendation_dataset.xlsx")
    # Convert comma-separated strings back to lists
    df['Courses'] = df['Courses'].apply(lambda x: [c.strip() for c in str(x).split(',')])
    df['Skills'] = df['Skills'].apply(lambda x: [s.strip() for s in str(x).split(',')])
    df['Interests'] = df['Interests'].apply(lambda x: [i.strip() for i in str(x).split(',')])
    return df

def recommend_careers(df, education, course, selected_interests, selected_skills):
    scores = []
    
    for _, row in df.iterrows():
        score = 0
        # Match course
        if course in row["Courses"]:
            score += 5
        
        # Match interests
        interest_matches = set(selected_interests).intersection(set(row["Interests"]))
        score += len(interest_matches) * 3
        
        # Match skills
        skill_matches = set(selected_skills).intersection(set(row["Skills"]))
        score += len(skill_matches) * 2
        
        if score > 0:
            scores.append({
                "career": row["Career"],
                "score": score,
                "matched_interests": list(interest_matches),
                "matched_skills": list(skill_matches)
            })
    
    # Sort by score descending
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:3]  # Return top 3 recommendations

def main():
    st.set_page_config(page_title="Career Recommendation System", page_icon="🎓", layout="wide")
    
    st.title("🎓 Career Recommendation System")
    st.markdown("""
    Welcome to the Career Recommendation System! Fill in your details below to get personalized career suggestions.
    """)
    
    try:
        df = load_data()
        
        # Extract unique values for selection
        all_courses = sorted(list(set([course for sublist in df['Courses'] for course in sublist])))
        all_skills = sorted(list(set([skill for sublist in df['Skills'] for skill in sublist])))
        all_interests = sorted(list(set([interest for sublist in df['Interests'] for interest in sublist])))
        education_levels = ["High School", "Undergraduate", "Postgraduate", "PhD"]

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Academic Background")
            education = st.selectbox("Select your Education Level", education_levels)
            course = st.selectbox("Select your Course/Major", all_courses)
            
        with col2:
            st.subheader("Personal Profile")
            selected_interests = st.multiselect("Select your Interests", all_interests)
            selected_skills = st.multiselect("Select your Skills", all_skills)
            
        if st.button("Get Recommendations"):
            if not selected_interests or not selected_skills:
                st.warning("Please select at least one interest and one skill for better recommendations.")
            else:
                recommendations = recommend_careers(df, education, course, selected_interests, selected_skills)
                
                if recommendations:
                    st.success("Here are your top career recommendations:")
                    for i, rec in enumerate(recommendations):
                        with st.expander(f"#{i+1}: {rec['career']}"):
                            st.write(f"**Match Score:** {rec['score']}")
                            if rec['matched_interests']:
                                st.write(f"**Matched Interests:** {', '.join(rec['matched_interests'])}")
                            if rec['matched_skills']:
                                st.write(f"**Matched Skills:** {', '.join(rec['matched_skills'])}")
                            
                            st.info(f"Based on your background in {course} and your profile, a career as a {rec['career']} would be a great fit!")
                else:
                    st.error("Sorry, we couldn't find a specific match. Try selecting more interests or skills.")

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure 'career_recommendation_dataset.xlsx' is in the same directory as the app.")

    st.sidebar.title("About")
    st.sidebar.info("""
    This system uses an Excel-based dataset to suggest careers based on:
    - Educational Background
    - Academic Course
    - Personal Interests
    - Technical/Soft Skills
    """)

if __name__ == "__main__":
    main()
