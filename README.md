# Plutarch

Hi, this is my project for the Insight Data Science Fellowship. Plutarch is a history podcast recommender, using word embeddings to find relevant topics to users search queries. In other words, Plutarch looks at commonly associated words to find new content related to what you're interested in. Check it out on www.plutarch.xyz!

The code is built as follows 

#Step 1: Get list of history podcasts off iTunes
- iTunes_scrape.ipynb

#Step 2: Pull podcast episodes from their respective RSS feeds
- get_episodes.ipynb

#Step 3: Clean up the podcast episode content, create a vocabulary database, and get the search prototype up and running
- clean_process.ipynb

#Step 4: Host on AWS and enjoy!
- flaskapp folder
