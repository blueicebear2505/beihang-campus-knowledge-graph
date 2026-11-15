import streamlit.components.v1 as components
from pyvis.network import Network
import csv
from PIL import Image
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from graph_model import load_csv, build_graph


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Beihang Hangzhou Campus",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. CUSTOM WEBSITE STYLING
# ==========================================
st.markdown("""
<style>
    .stApp {
    background-color: #F5F7FB;
}

/* Main page headings */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4 {
    color: #17243A !important;
}

/* Main page paragraphs and descriptions */
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stCaptionContainer"],
[data-testid="stMain"] label {
    color: #17243A !important;
}
/* About page technology list */
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li *,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] ul {
    color: #17243A !important;
    -webkit-text-fill-color: #17243A !important;
}
/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E5EAF1;
    padding: 18px;
    border-radius: 12px;
}

/* Metric numbers */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #23466E !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #17243A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Main page buttons */
.stButton button,
.stButton button * {
    color: #FFFFFF !important;
    background-color: #17365D !important;
    border-color: #17365D !important;
    font-weight: 600 !important;
}

.stButton button:hover,
.stButton button:hover * {
    color: #FFFFFF !important;
    background-color: #24558A !important;
    border-color: #24558A !important;
}

/* Overview buttons: force white text */
[data-testid="stMain"] div[data-testid="stButton"] button,
[data-testid="stMain"] div[data-testid="stButton"] button *,
[data-testid="stMain"] div[data-testid="stButton"] button p {
    color: #FFFFFF !important;
}

[data-testid="stMain"] div[data-testid="stButton"] button {
    background-color: #17365D !important;
    border-color: #17365D !important;
}

[data-testid="stMain"] div[data-testid="stButton"] button:hover {
    background-color: #24558A !important;
}
/* Chat message text */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em {
    color: #17243A !important;
    -webkit-text-fill-color: #17243A !important;
} 
/* Selected value inside the dropdown bar */
[data-testid="stSelectbox"] [data-baseweb="select"] div[class*="singleValue"] {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Dropdown menu options */
[role="listbox"] [role="option"] {
    color: #17243A !important;
    -webkit-text-fill-color: #17243A !important;
    background-color: #FFFFFF !important;
}
/* Inline code inside AI chat responses */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {
    color: #FFFFFF !important;
    background-color: #34445A !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD CAMPUS DATA
# ==========================================

def get_data():

    locations = load_csv("locations_checked.csv")
    relationships = load_csv("relationships_checked.csv")
    sources = load_csv("sources.csv")

    nodes, graph = build_graph(
        locations,
        relationships
    )

    return locations, relationships, sources, nodes, graph


try:

    locations, relationships, sources, nodes, graph = get_data()

except FileNotFoundError as e:

    st.error(f"Could not find a required CSV file: {e}")
    st.stop()

def set_page(target):
    st.session_state["selected_page"] = target

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("# BEIHANG")

st.sidebar.caption(
    "HANGZHOU INTERNATIONAL CAMPUS"
)

st.sidebar.divider()

st.sidebar.markdown("### CAMPUS EXPLORER")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Campus Map",
        "Knowledge Graph",
        "Location Explorer",
        "Find a Route",
        "AI Assistant",
        "About"
    ],
    label_visibility="collapsed",
    key="selected_page"
)

st.sidebar.divider()

st.sidebar.caption(
    "AI + X PROJECT | 2026"
)


# ==========================================
# 5. CALCULATE DASHBOARD STATISTICS
# ==========================================

total_locations = len(nodes)

total_connections = sum(
    len(neighbors)
    for neighbors in graph.values()
) // 2

connected_places = len(graph)



# ==========================================
# 6. OVERVIEW PAGE
# ==========================================

if page == "Overview":

    st.markdown(
        '<p class="main-title">Beihang Campus Explorer</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">'
        'Hangzhou International Campus | '
        'Knowledge Graph & Navigation System'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Campus Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Locations", total_locations)
    col2.metric("Total Connections", total_connections)
    col3.metric("Connected Places", connected_places)

    st.divider()

    st.markdown("### Explore the Campus")

    # Shared card styling
    card_style = (
        "background-color: #ffffff;"
        "border: 1px solid #dbe4ee;"
        "border-radius: 12px;"
        "padding: 20px;"
        "min-height: 145px;"
    )

    # First row
    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
        <div style="{card_style}">
            <h3 style="color:#23466E;">Campus Map</h3>
            <p style="color:#526477;">
                Explore buildings and facilities
                on the actual Hangzhou campus map.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open Campus Map",
            use_container_width=True,
            on_click=set_page,
            args=("Campus Map",)
        )

    with col2:

        st.markdown(f"""
        <div style="{card_style}">
            <h3 style="color:#23466E;">Knowledge Graph</h3>
            <p style="color:#526477;">
                Discover how campus locations
                connect to one another.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open Knowledge Graph",
            use_container_width=True,
            on_click=set_page,
            args=("Knowledge Graph",)
        )

    st.write("")

    # Second row
    col3, col4 = st.columns(2)

    with col3:

        st.markdown(f"""
        <div style="{card_style}">
            <h3 style="color:#23466E;">Location Explorer</h3>
            <p style="color:#526477;">
                Search locations and inspect
                their information and relationships.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Explore Locations",
            use_container_width=True,
            on_click=set_page,
            args=("Location Explorer",)
        )

    with col4:

        st.markdown(f"""
        <div style="{card_style}">
            <h3 style="color:#23466E;">Find a Route</h3>
            <p style="color:#526477;">
                Find connections between
                two campus locations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Find a Route",
            use_container_width=True,
            on_click=set_page,
            args=("Find a Route",)
        )

    st.write("")

    # Third row: AI Assistant
    col5, col6 = st.columns(2)

    with col5:

        st.markdown(f"""
        <div style="{card_style}">
            <h3 style="color:#23466E;">AI Assistant</h3>
            <p style="color:#526477;">
                Ask questions about campus facilities,
                locations, services and navigation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open AI Assistant",
            use_container_width=True,
            on_click=set_page,
            args=("AI Assistant",)
        )

# ==========================================
# 7. CAMPUS MAP PAGE
# ==========================================

elif page == "Campus Map":

    from PIL import ImageDraw, ImageFont

    st.title("Interactive Campus Map")

    st.write(
        "Select a campus location to highlight it on the map "
        "and view its information."
    )

    # Get all locations from the main location dataset
    location_data = {
        loc["id"]: loc
        for loc in locations
        if loc.get("id")
    }

    saved_centres = []

    try:
        with open(
            "building_centers.csv",
            "r",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                location_id = row.get("id", "").strip()

                # Ignore locations that are not in our dataset
                # Also exclude the generic duplicate dormitory record
                if location_id not in location_data or location_id == "L04":
                    continue

                saved_centres.append({
                    "id": location_id,
                    "name": location_data[location_id]["name"],
                    "x": float(row["x"]),
                    "y": float(row["y"])
                })

    except FileNotFoundError:
        st.error("building_centers.csv was not found.")

    if saved_centres:

        # Dropdown selector
        selected_id = st.selectbox(
            "Choose a campus location",
            [item["id"] for item in saved_centres],
            format_func=lambda x: (
                f"{location_data[x]['name']} ({x})"
            )
        )

        # Load campus map
        map_image = Image.open(
            "hangzhoubeihang.jpg"
        ).convert("RGB")

        draw = ImageDraw.Draw(map_image)
        font = ImageFont.load_default()

        # Draw all saved location markers
        for building in saved_centres:

            x = int(
                building["x"] / 100 * map_image.width
            )

            y = int(
                building["y"] / 100 * map_image.height
            )

            if building["id"] == selected_id:

                # Outer highlight
                draw.ellipse(
                    (
                        x - 32,
                        y - 32,
                        x + 32,
                        y + 32
                    ),
                    fill="#ffb3b3",
                    outline="white",
                    width=4
                )

                # Selected marker
                draw.ellipse(
                    (
                        x - 20,
                        y - 20,
                        x + 20,
                        y + 20
                    ),
                    fill="#ff3333",
                    outline="white",
                    width=4
                )

            else:

                # Normal markers
                draw.ellipse(
                    (
                        x - 12,
                        y - 12,
                        x + 12,
                        y + 12
                    ),
                    fill="red",
                    outline="white",
                    width=3
                )

            # Display location ID
            draw.text(
                (x + 18, y - 12),
                building["id"],
                fill="blue",
                font=font,
                stroke_width=2,
                stroke_fill="white"
            )

        st.write(
            f"**Locations displayed:** {len(saved_centres)}"
        )

        # Display map
        st.image(
            map_image,
            width=800
        )

        # Display selected location information
        selected_location = location_data[selected_id]

        st.divider()

        st.subheader(selected_location["name"])

        col1, col2 = st.columns(2)

        col1.metric("Location ID", selected_id)

        col2.metric(
            "Category",
            selected_location.get("category", "Unknown")
        )

        st.write(
            "**Entity Type:**",
            selected_location.get("entity_type", "Unknown")
        )

        st.write(
            "**Evidence:**",
            selected_location.get("evidence", "Unknown")
        )

    else:

        st.warning(
            "No valid location coordinates have been saved yet."
        )

# ==========================================
# 8. KNOWLEDGE GRAPH PAGE
# ==========================================

elif page == "Knowledge Graph":

    st.title("Interactive Knowledge Graph")

    st.write(
        "Explore relationships between buildings "
        "and facilities at Beihang University."
    )

    # Graph statistics
    col1, col2 = st.columns(2)

    col1.metric("Nodes", len(nodes))

    # Count unique connections
    unique_edges = {}

    for source, neighbors in graph.items():
        for target, distance, relationship in neighbors:

            edge_key = tuple(sorted([source, target]))

            unique_edges[edge_key] = (
                distance,
                relationship
            )

    col2.metric("Connections", len(unique_edges))

    st.divider()

    st.subheader("Campus Relationship Network")

    st.write(
        "Drag nodes to rearrange the network. "
        "Zoom in and out to explore connections. "
        "Hover over a node to see its information."
    )

    # Create PyVis network
    net = Network(
        height="650px",
        width="100%",
        directed=False,
        bgcolor="#ffffff",
        font_color="#222222"
    )

    # Color nodes by category
    category_colors = {
        "Academic": "#4285F4",
        "Residential": "#34A853",
        "Sports": "#FBBC04",
        "Dining": "#EA4335",
        "Research": "#9C27B0",
        "Study": "#00ACC1",
        "Services": "#FF7043"
    }

    # Add all campus locations as nodes
    for node_id, info in nodes.items():

        name = info.get("name", node_id)

        category = info.get(
            "category", "Other"
        )

        entity_type = info.get(
            "entity_type", "Unknown"
        )

        color = category_colors.get(
            category, "#78909C"
        )

        tooltip = (
            f"Name: {name}<br>"
            f"ID: {node_id}<br>"
            f"Category: {category}<br>"
            f"Type: {entity_type}"
        )

        net.add_node(
            node_id,
            label=name,
            title=tooltip,
            color=color,
            size=20
        )

    # Add relationships as edges
    for (source, target), (distance, relationship) in unique_edges.items():

        edge_label = relationship.replace("_", " ")

        if distance is not None:
            edge_label += f" ({distance:g} m)"

        net.add_edge(
            source,
            target,
            label=edge_label,
            title=f"Relationship: {relationship}"
        )

    # Configure network layout
    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=150,
        spring_strength=0.04,
        damping=0.09
    )

    net.show_buttons(
        filter_=["physics"]
    )

    # Display interactive graph
    graph_html = net.generate_html()

    components.html(
        graph_html,
        height=700,
        scrolling=True
    )

# ==========================================
# 9. LOCATION EXPLORER PAGE
# ==========================================

elif page == "Location Explorer":

    st.title("Location Explorer")

    st.write(
        "Search and inspect locations "
        "within the Hangzhou campus."
    )

    search = st.text_input(
        "Search location",
        placeholder="Enter a building or facility name..."
    )

    categories = sorted(set(
        loc.get("category", "")
        for loc in locations
        if loc.get("category")
    ))

    category_filter = st.selectbox(
        "Filter by category",
        ["All"] + categories
    )

    route_only = st.checkbox(
        "Show main route nodes only"
    )

    filtered_locations = []

    for loc in locations:
        if loc.get("id") == "L04":
            continue

        name = loc.get("name", "")
        category = loc.get("category", "")
        route_node = loc.get(
            "is_route_node", ""
        ).lower()

        if search.lower() not in name.lower():
            continue

        if (
            category_filter != "All"
            and category != category_filter
        ):
            continue

        if route_only and route_node != "yes":
            continue

        filtered_locations.append(loc)

    if filtered_locations:

        location_ids = [
            loc["id"]
            for loc in filtered_locations
        ]

        selected_id = st.selectbox(
            "Select a campus location",
            location_ids,
            format_func=lambda x: (
                f"{nodes[x].get('name', x)} ({x})"
            )
        )

        selected_location = nodes[selected_id]

        st.divider()

        st.subheader(
            selected_location.get(
                "name", selected_id
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Location ID:**", selected_id)

            st.write(
                "**Entity Type:**",
                selected_location.get(
                    "entity_type", "Unknown"
                )
            )

            st.write(
                "**Category:**",
                selected_location.get(
                    "category", "Unknown"
                )
            )

        with col2:

            st.write(
                "**Verification Status:**",
                selected_location.get(
                    "verification_status", "Unknown"
                )
            )

            st.write(
                "**Main Route Node:**",
                selected_location.get(
                    "is_route_node", "Unknown"
                )
            )

        st.write(
            "**Evidence Sources:**",
            selected_location.get(
                "evidence", "Not available"
            )
        )

        st.divider()

        
        st.subheader("Connected Locations")

        neighbors = graph.get(selected_id, [])

        # Only show physical walking connections
        connected_neighbors = [
            (neighbor_id, distance)
            for neighbor_id, distance, relationship in neighbors
            if relationship == "CONNECTED_TO"
        ]

        if connected_neighbors:

            connection_data = []

            for neighbor_id, distance in connected_neighbors:

                neighbor_name = nodes.get(
                    neighbor_id, {}
                ).get("name", "Unknown")

                connection_data.append({
                    "Location ID": neighbor_id,
                    "Location Name": neighbor_name,
                    "Distance (m)": (
                        distance
                        if distance is not None
                        else "Not available"
                    )
                })

            st.dataframe(
                connection_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No CONNECTED_TO relationships found."
            )


        st.divider()

        st.subheader("All Relationships")

        related_data = []

        for rel in relationships:

            subject = rel.get("subject_id", "")
            target = rel.get("target_id", "")

            if (
                subject == selected_id
                or target == selected_id
            ):

                related_data.append({
                    "Subject": subject,
                    "Relationship": rel.get(
                        "relationship", ""
                    ),
                    "Target": target,
                    "Distance (m)": rel.get(
                        "distance_m", ""
                    ),
                    "Verification": rel.get(
                        "verification_status", ""
                    )
                })

        if related_data:

            st.dataframe(
                related_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No relationships found.")

    else:

        st.warning("No matching locations found.")



# ==========================================
# 10. ROUTE FINDER PAGE
# ==========================================

elif page == "Find a Route":

    import networkx as nx

    st.title("Campus Route Finder")

    st.write(
        "Find the shortest available route "
        "between two campus locations."
    )

    st.warning(
        "Route distances are estimates and may not "
        "represent actual walking paths."
    )

    # Build a separate graph using only walking connections
    route_graph = nx.Graph()

    for source, neighbors in graph.items():

        for target, distance, relationship in neighbors:

            if relationship != "CONNECTED_TO":
                continue

            if distance is None:
                continue

            route_graph.add_edge(
                source,
                target,
                weight=distance
            )

    # Keep only physical locations that have route connections
    route_locations = [
        location_id
        for location_id in route_graph.nodes
        if location_id in nodes
        and nodes[location_id].get("entity_type") != "Category"
        and location_id != "L04"
    ]

    route_locations.sort(
        key=lambda x: nodes[x].get("name", x)
    )

    if len(route_locations) >= 2:

        col1, col2 = st.columns(2)

        with col1:

            start_id = st.selectbox(
                "Starting location",
                route_locations,
                format_func=lambda x: (
                    f"{nodes[x].get('name', x)} ({x})"
                ),
                key="route_start"
            )

        with col2:

            end_options = [
                location_id
                for location_id in route_locations
                if location_id != start_id
            ]

            end_id = st.selectbox(
                "Destination",
                end_options,
                format_func=lambda x: (
                    f"{nodes[x].get('name', x)} ({x})"
                ),
                key="route_end"
            )

        if st.button("Find Shortest Route"):

            try:

                route = nx.shortest_path(
                    route_graph,
                    source=start_id,
                    target=end_id,
                    weight="weight",
                    method="dijkstra"
                )

                total_distance = nx.shortest_path_length(
                    route_graph,
                    source=start_id,
                    target=end_id,
                    weight="weight",
                    method="dijkstra"
                )

                st.success("Route found!")

                st.subheader("Your Route")

                for index, location_id in enumerate(route):

                    location_name = nodes[location_id].get(
                        "name", location_id
                    )

                    st.write(
                        f"**{index + 1}.** {location_name} "
                        f"({location_id})"
                    )

                    if index < len(route) - 1:
                        st.write("↓")

                st.divider()

                col1, col2 = st.columns(2)

                col1.metric(
                    "Total Distance",
                    f"{total_distance:.0f} m"
                )

                col2.metric(
                    "Locations",
                    len(route)
                )

                st.caption(
                    "The distance is calculated from estimated "
                    "CONNECTED_TO distances in the dataset."
                )

            except nx.NetworkXNoPath:

                st.error(
                    "No route exists between these locations."
                )

    else:

        st.warning(
            "Not enough connected locations are available "
            "to calculate a route."
        )

# ==========================================
# 11. AI ASSISTANT PAGE
# ==========================================

elif page == "AI Assistant":

    from google import genai

    st.markdown(
        "<h1 style='color:#17243A;'>AI Campus Assistant</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#17243A;'>Ask questions about Beihang's Hangzhou International Campus.</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#526477; font-size:14px;'>Powered by Google Gemini</p>",
        unsafe_allow_html=True
    )

    # Initialize chat history
    if "campus_chat_history" not in st.session_state:
        st.session_state.campus_chat_history = []

    # Display previous messages
    for message in st.session_state.campus_chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Question input
    user_question = st.chat_input(
        "Ask something about the campus..."
    )

    if user_question:

        # Display user's question
        with st.chat_message("user"):
            st.markdown(user_question)

        st.session_state.campus_chat_history.append({
            "role": "user",
            "content": user_question
        })

        # Prepare campus information
        campus_context = "CAMPUS LOCATIONS:\n"

        for loc in locations:

            campus_context += (
                f"- ID: {loc.get('id')}, "
                f"Name: {loc.get('name')}, "
                f"Category: {loc.get('category')}, "
                f"Type: {loc.get('entity_type')}\n"
            )

        campus_context += "\nCAMPUS RELATIONSHIPS:\n"

        for rel in relationships:

            campus_context += (
                f"- {rel.get('subject_id')} "
                f"{rel.get('relationship')} "
                f"{rel.get('target_id')}, "
                f"Distance: {rel.get('distance_m', 'Unknown')} m\n"
            )

        # Include recent conversation history
        conversation = ""

        for message in st.session_state.campus_chat_history[-10:]:

            conversation += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

        # Create prompt for Gemini
        prompt = f"""
You are the AI Campus Assistant for Beihang University
Hangzhou International Campus.

Answer questions using the campus information below.

Rules:
1. Use the supplied campus data as your main reference.
2. Do not invent building locations, facilities, or distances.
3. If the information is unavailable, say so clearly.
4. Explain campus relationships in simple language.
5. For route questions, only use CONNECTED_TO relationships.
6. Explain that route distances are estimates.
7. Be concise and helpful.

CAMPUS DATA:

{campus_context}

CONVERSATION HISTORY:

{conversation}

Answer the latest user question.
"""

        # Ask Gemini
        with st.chat_message("assistant"):

            with st.spinner("Gemini is thinking..."):

                try:

                    client = genai.Client(
                        api_key=st.secrets["GEMINI_API_KEY"]
                    )

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                    answer = response.text

                    if not answer:
                        answer = "Gemini returned an empty response."

                    st.markdown(answer)

                    st.session_state.campus_chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(
                        "Sorry, I couldn't get an answer from Gemini."
                    )

                    st.caption(f"Error details: {e}")

    # Clear conversation button
    if st.session_state.campus_chat_history:

        if st.button("Clear Conversation"):

            st.session_state.campus_chat_history = []

            st.rerun()

# ==========================================
# 12. ABOUT PAGE
# ==========================================

elif page == "About":

    st.title("About This Project")

    st.write(
        "Beihang Campus Knowledge Graph is an "
        "AI+X project designed to organize and "
        "explore information about Beihang University's "
        "Hangzhou International Campus."
    )

    st.subheader("Project Technologies")

    st.markdown("""
    - Python
    - Streamlit
    - Pandas
    - NetworkX
    - PyVis
    - Folium
    """)

    st.subheader("Data Sources")

    st.dataframe(
        sources,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 13. FOOTER
# ==========================================
st.divider()

st.markdown(
    """
    <div style="
        color: #526477;
        -webkit-text-fill-color: #526477;
        text-align: center;
        font-size: 13px;
    ">
        Beihang University | Hangzhou International Campus | AI+X Project
    </div>
    """,
    unsafe_allow_html=True
)