# Beihang Campus Knowledge Graph

An AI-powered campus information system designed to organise, explore and connect information about Beihang University Hangzhou International Campus.

## Project Overview

The Beihang Campus Knowledge Graph uses structured data and graph-based relationships to represent campus information.

Instead of treating campus information as separate entries, the system connects locations, buildings, facilities and other campus-related entities through relationships.

The project aims to make campus information easier to explore, understand and navigate.

## Main Features

### 1. Overview
Provides an introduction to the project and its main functions.

### 2. Campus Map
Displays campus locations and their geographical information.

### 3. Knowledge Graph
Visualises connections between different campus entities and their relationships.

### 4. Location Explorer
Allows users to explore individual campus locations and related information.

### 5. Route Finder
Helps users explore connections and routes between campus locations.

### 6. AI Assistant
Uses Google's Gemini API to answer questions about campus information.

### 7. About
Provides information about the project and its development.

## Technologies Used

- Python
- Streamlit
- Pandas
- NetworkX
- PyVis
- Google Gemini API
- CSV for structured data storage
- Git and GitHub for version control

## Project Structure

```text
beihang_campus_kg/
│
├── app.py
├── graph_model.py
├── load_data.py
│
├── sources.csv
├── relationships_checked.csv
├── locations_checked.csv
├── building_centers.csv
├── map_coordinates.csv
│
├── requirements.txt
├── hangzhoubeihang.jpg
│
└── .streamlit/
    └── secrets.toml
```

Note: `secrets.toml` is stored locally and is excluded from the GitHub repository.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/blueicebear2505/beihang-campus-knowledge-graph.git
```

### 2. Enter the project directory

```bash
cd beihang-campus-knowledge-graph
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a folder named `.streamlit` in the project directory.

Inside it, create a file named `secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key.

Never upload this file or share your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your web browser.

## Data Organisation

The project uses CSV files to organise campus information.

- Sources: Records the information sources used by the project.
- Relationships: Stores connections between campus entities.
- Locations: Stores geographical and location-related information.
- Building coordinates: Supports campus map visualisation.

The data structure supports the construction and exploration of the campus knowledge graph.

## Project Objective

This project demonstrates how artificial intelligence, structured data and graph theory can be combined to organise campus information and create an interactive campus exploration system.

## Author

Developed as an AI+X creative project at Beihang University Hangzhou International Campus.