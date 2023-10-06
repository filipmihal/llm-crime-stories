import gensim.downloader
from gensim.models import KeyedVectors
import hashlib
from typing import List, Optional
from weaviate import Client as DbClient

Theme = List[str]
WordEmbedding = List[float]

def get_word2vec() -> KeyedVectors:
    return KeyedVectors.load('./models/word2vec.gn300.wordvectors', mmap='r')

def generate_themes(count: int) -> List[Theme]:
    wv = get_word2vec()
    # the 1 is there because <s> is the first token (eos)
    return [wv.index_to_key[i * 3 + 1: i * 3 + 3 + 1] for i in range(count)]

def get_vectors(themes: List[Theme]) -> List[WordEmbedding]:
    # FOR THE FIRST TIME YOU HAVE TO DOWNLOAD THIS I BELIEVE (there is an api somewhere, that could work? -\_/-)
    # google_news_kv = gensim.downloader.load('word2vec-google-news-300')
    # google_news_kv.save("word2vec.gn300.wordvectors")

    wv = get_word2vec()
    return [[float(val) for val in wv[word]] for theme in themes for word in theme]

    

def create_schema(client: DbClient) -> None:
    schema = {
        "classes": [
            {
                "class": "StoryTheme",
                "vectorizer": "none",
                "properties": [
                    {
                        "name": "thematic_keywords",
                        "dataType": ["text[]"]
                    }
                ]
            }
        ]
    }
    
    try:
        client.schema.create(schema)
        print("Schema created")
    except Exception as e:
        print("Schema already exists", e)

def generate_id(theme: Theme) -> str:
    """
    Different items are very unlikely to have the same id.
    Same items are going to have same id every time.
    
    Should be sufficient.
    """
    return hashlib.sha256(''.join(theme).encode()).hexdigest()

def import_themes(client: DbClient, themes: List[Theme], vectors: List[WordEmbedding]) -> None:
    for theme, vector in zip(themes, vectors):
        theme_obj = {
            "class": "StoryTheme",
            "properties": {
                "thematic_keywords": theme
            }
        }
        
        try:
            client.data_object.create(theme_obj, class_name="StoryTheme", vector=vector)
            print(f'Theme added')
        except Exception as e:
            print(f'Erorr adding a theme {theme_obj["id"]}: {str(e)}')

def create_client() -> Optional[DbClient]:
    client = DbClient("http://localhost:8080")

    try:
        client.is_live()
        print("Connected to Weaviate!")
        return client
    except Exception as e:
        print("Cannot connect to Weaviate!", e)
        return None

def query_all_story_themes(client: DbClient) -> None:
    # Define a GraphQL query to retrieve all StoryThemes
    query = """
    {
        Get {
            StoryTheme {
                thematic_keywords
            }
        }
    }
    """
    
    try:
        # Execute the query
        results = client.query.graphql(query)
        
        # Output the results
        print("Query Results:", results)
    except Exception as e:
        print("Error querying themes:", str(e))

if __name__ == "__main__":
    client = create_client()
    # create_schema(client)
    
    # themes = generate_themes(2)
    # themes_we = get_vectors(themes)
    
    # import_themes(client, themes, themes_we)
    
    result = client.query.get("StoryTheme", ["thematic_keywords"]).do()
    print(result)