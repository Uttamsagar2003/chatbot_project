import requests
from bs4 import BeautifulSoup
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

def extract_course_data():
    url = "https://brainlox.com/courses/category/technical"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    courses = []
    
    # Extract course data
    course_overviews = soup.find_all("div", class_="courses-overview")
    for overview in course_overviews:
        title_element = overview.find("h3")
        title = title_element.text.strip() if title_element else "No title found"
        description_element = overview.find("p")
        description = description_element.text.strip() if description_element else "No description found"
        
        courses.append({"title": title, "description": description})

    print(f"Extracted {len(courses)} courses.")
    return courses

def create_vector_store(course_data):
    if not course_data:
        print("No course data to process.")
        return None

    # Using SentenceTransformer for embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    texts = [course['description'] for course in course_data]

    # Create vector store using Chroma
    vector_store = Chroma.from_texts(texts, embeddings)
    return vector_store
