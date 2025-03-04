import requests
import json
import time
from tqdm import tqdm  # For progress bar

def get_all_authors():
    """Get list of all authors from the API"""
    response = requests.get("https://poetrydb.org/author")
    if response.status_code == 200:
        return response.json()["authors"]
    else:
        print(f"Error fetching authors: {response.status_code}")
        return []

def get_titles_by_author(author):
    """Get all titles for a specific author"""
    url = f"https://poetrydb.org/author/{author}/title"
    response = requests.get(url)
    if response.status_code == 200:
        return [poem["title"] for poem in response.json()]
    else:
        print(f"Error fetching titles for {author}: {response.status_code}")
        return []

def get_poem(author, title):
    """Get specific poem by author and title"""
    encoded_author = requests.utils.quote(author)
    encoded_title = requests.utils.quote(title)
    url = f"https://poetrydb.org/author,title/{encoded_author};{encoded_title}"
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                print(f"Unexpected response format for '{title}' by {author}")
                return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON for '{title}' by {author}")
            return None
    else:
        print(f"Error fetching poem '{title}' by {author}: {response.status_code}")
        return None

def main():
    poetry_data = {
        "poems": [],
        "sent": []
    }
    
    print("Fetching list of authors...")
    authors = get_all_authors()
    print(f"Found {len(authors)} authors")
    
    for author in tqdm(authors, desc="Processing authors"):
        titles = get_titles_by_author(author)
        time.sleep(0.1)
        
        for title in titles:
            poem = get_poem(author, title)
            
            if poem and isinstance(poem, list) and len(poem) > 0:
                try:
                    poem_entry = poem[0]
                    
                    # Check linecount existence and validity
                    if 'linecount' not in poem_entry:
                        print(f"No linecount for '{title}' by {author}, skipping.")
                        continue
                    try:
                        linecount = int(poem_entry['linecount'])
                    except ValueError:
                        print(f"Invalid linecount '{poem_entry['linecount']}' for '{title}' by {author}, skipping.")
                        continue
                    if linecount >= 69:
                        continue  # Skip poems with 69 or more lines
                    
                    # Create unique ID
                    safe_author = author.replace(" ", "_").replace(";", "_").replace("/", "_")
                    safe_title = title.replace(" ", "_").replace(";", "_").replace("/", "_")
                    unique_id = f"{safe_author}-{safe_title}"
                    
                    poem_entry["id"] = unique_id
                    poem_entry["sent"] = False
                    
                    poetry_data["poems"].append(poem_entry)
                except (IndexError, KeyError) as e:
                    print(f"Error processing poem '{title}' by {author}: {e}")
                    print(f"Poem data: {poem}")
            
            time.sleep(0.01)
    
    # Save to the new file
    with open("short_poetries.json", "w", encoding="utf-8") as f:
        json.dump(poetry_data, f, indent=2)
    
    print(f"Successfully saved {len(poetry_data['poems'])} poems to short_poetries.json")

if __name__ == "__main__":
    main()