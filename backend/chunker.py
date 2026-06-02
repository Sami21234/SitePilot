from langchain_text_splitters import RecursiveCharacterTextSplitter     # handles all edge cases like -> span boundaries, paragraph of varying length
'''
example -->
1000 character article, then...

Chunk 1 (400 chars)
Chunk 2 (400 chars)
Chunk 3 (300 chars)

'''


# function to chunk the pages 

def chunk_pages(pages, chunk_size = 400, chunk_overlap = 50):

    """
    Takes crawled pages and returns clean chunks
    ready for embedding.

    Args:
        pages: list of dicts with 'url', 'title', 'text'
        chunk_size: max characters per chunk
        chunk_overlap: characters repeated between chunks

    Returns:
        list of dicts with 'text', 'source', 'title'
    """

    splitter = RecursiveCharacterTextSplitter(     # creartes the splitting object.
        chunk_size = chunk_size,        # Uses 400 characters.
        chunk_overlap = chunk_overlap,
        separators = ["\n\n", "\n", ". ", " ", ""]      # It is very important step --> It tries to split in this order:
                                                     
    )

    '''
        Paragraph break -> "\n\n"
        Single line break -> "\n"
        Sentence ending -> ". "
        Space -> ""
    '''

    all_chunks = []     # Stores all generated chunks.

    for page in pages:      # Processes each crawled page
        if not page.get("text"):
            continue

        chunks = splitter.split_text(page["text"])      # splitting text

        # Loop Through Chunks

        for i, chunk in enumerate(chunks):      # enumerate() gives index + value.

            '''
            example:

                i=0
                chunk="text 1"

                i=1
                chunk="text 2"
            '''

            chunk = chunk.strip()       # removes extra spaces

            if len(chunk) < 30:         # skipping small and useless chunks
                continue

            # Now, storing the chunks into the list called --> all_chunks

            all_chunks.append({
                "text": chunk,      # Actual content
                "source": page["url"],      # from Where chunk came from
                "title": page.get("title", ""),     # Page title
                "chunk_index": i
            })

    return all_chunks

if __name__ == "__main__":

    from crawler import crawl_website       # importing crawler function 

    pages = crawl_website(
        "https://books.toscrape.com",
        max_pages=5
    )

    # Converting pages into chunks
    chunks = chunk_pages(pages)

    print(f"\nTotal pages crawled: {len(pages)}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Average chunks per page: {len(chunks)/len(pages):.1f}")

    print("\n" + "="*60)
    print("SAMPLE CHUNKS:")
    print("="*60)

    for i, chunk in enumerate(chunks[:3]):      # printing the chunks
        print(f"\nChunk {i+1}:")
        print(f"Source : {chunk['source']}")
        print(f"Title  : {chunk['title']}")
        print(f"Index  : {chunk['chunk_index']}")
        print(f"Length : {len(chunk['text'])} chars")
        print(f"Text   : {chunk['text'][:200]}")
        print("-"*60)