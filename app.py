import streamlit as st
import pandas as pd

st.set_page_config(page_title="Restaurant Recommender", layout="wide")

st.markdown("""
<style>

/* Main page background */
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;

}
            
.block-container{
background: rgba(255,255,255,0.85);
backdrop-filter: blur(1px);
padding: 2rem;
border-radius: 20px;
box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
margin-top: 20px;
}
            
.badge-container{
display:flex;
justify-content:center;
align-items:center;
gap:20px;
margin-top:50px;
margin-bottom:15px;
}

.badge{
padding:6px 14px;
border-radius:20px;
color:black;
font-size:15px;
font-weight:600;
background:#f5f5f5;
box-shadow:0px 2px 6px rgba(0,0,0,0.15);
}           

.restaurant-card{
background: rgba(255,255,255,0.95);
padding:25px;
border-radius:18px;
box-shadow:0px 8px 25px rgba(0,0,0,0.25);
margin-bottom:25px;
transition:0.3s;
}

.restaurant-card:hover{
transform:scale(1.02);
box-shadow:0px 10px 30px rgba(0,0,0,0.35);
}

.restaurant-name{
font-size:24px;
font-weight:600;
color:black;
margin-bottom:8px;
}
                        
/* Sidebar background */
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#141e30,#243b55);
}

/* Sidebar text visibility */
[data-testid="stSidebar"] label {
color: white !important;
}

[data-testid="stSidebar"] .stSelectbox span {
color: white !important;
}

[data-testid="stSidebar"] .stMultiSelect span {
color: white !important;
}

[data-testid="stSidebar"] svg {
fill: white !important;
}

</style>
""", unsafe_allow_html=True)

# Load clustered data
df_clustered = pd.read_csv(r"C:\Users\ssarav569\Downloads\restaurant_recommender_system_prjct4-main_working\Restaurant_Recommender_System\clustered_data.csv")

# Recommendation Function
def recommend_by_cluster(restaurant_name, city=None, cuisines=None, cost_range=None, top_n=5):
    if restaurant_name not in df_clustered['name'].values:
        return pd.DataFrame(columns=['name', 'city', 'cuisine', 'rating', 'cost'])

    restaurant_index = df_clustered[df_clustered['name'] == restaurant_name].index[0]
    target_cluster = df_clustered.loc[restaurant_index, 'cluster']
    
    # Filter same cluster
    cluster_group = df_clustered[df_clustered['cluster'] == target_cluster]

    # Drop the restaurant itself
    cluster_group = cluster_group.drop(restaurant_index, errors='ignore')

    #  Apply Filters 
    if city and city != "All":
        cluster_group = cluster_group[cluster_group['city'].str.contains(city, case=False, na=False)]

    if cuisines and "All" not in cuisines:
        cluster_group = cluster_group[cluster_group['cuisine'].apply(
            lambda x: any(c in x for c in cuisines) if pd.notna(x) else False
        )]

    if cost_range and cost_range != "All":
        min_cost, max_cost = map(int, cost_range.split('-'))
        cluster_group = cluster_group[(cluster_group['cost'] >= min_cost) & (cluster_group['cost'] <= max_cost)]

    return cluster_group.head(top_n)[['name', 'city', 'cuisine', 'rating', 'cost']]

# Streamlit UI 
st.title("🍽️ Swiggy Restaurant Recommender")

# Dropdown for restaurant selection
restaurant_list = df_clustered['name'].dropna().unique()
restaurant_name = st.selectbox("Select a restaurant:", restaurant_list)

# Filters
st.sidebar.markdown("<h2 style='color:white;'>🔍 Filters</h2>", unsafe_allow_html=True)

# City filter
cities = ["All"] + sorted(df_clustered['city'].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Select City:", cities)

# Cuisine filter (multiselect)
all_cuisines = sorted(set(
    c.strip() for cuisines in df_clustered['cuisine'].dropna().str.split(",") for c in cuisines
))
selected_cuisines = st.sidebar.multiselect("Select Cuisine(s):", ["All"] + all_cuisines, default="All")

# Cost filter
cost_ranges = ["All", "0-200", "201-500", "501-1000", "1001-5000"]
selected_cost = st.sidebar.selectbox("Select Cost Range:", cost_ranges)


# Number of recommendations
top_n = st.slider("How many recommendations?", 1, 10, 5)

if st.button("Get Recommendations"):
    results = recommend_by_cluster(
        restaurant_name, 
        city=selected_city, 
        cuisines=selected_cuisines, 
        cost_range=selected_cost, 
        top_n=top_n
    )

    if results.empty:
        st.warning("⚠️ No recommendations found with the selected filters.")
    else:
        st.success(f"Here are {len(results)} restaurants similar to {restaurant_name}")

        for _, row in results.iterrows():

            st.markdown(f"""
            <div class="restaurant-card">

            <div class="restaurant-name">{row['name']}</div>

            <span class="badge city">📍 {row['city']}</span>
            <span class="badge cost">💰 ₹{row['cost']}</span>
            <span class="badge rating">⭐ {round(row['rating'],1)}</span>

            <br><br>

            🍜 <b>Cuisine:</b> {row['cuisine']}

            </div>
            """, unsafe_allow_html=True)