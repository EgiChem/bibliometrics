from pathlib import Path

import pandas as pd
import pybliometrics
from pybliometrics.scopus import AuthorRetrieval
from jinja2 import Environment, FileSystemLoader


# File system
file_path = Path(__file__).resolve()
root_path = file_path.parents[1]

# Initialize Scopus API connection
pybliometrics.scopus.init()


def get_author_docs(author_id: str, save_csv=True):
    """
    Get a list of document objects for a given author_id.
    """
    # Get author
    au = AuthorRetrieval(author_id)
    print(f"Retrieving documents for {au.initials} {au.surname}...")

    # Get author documents
    docs = au.get_documents()

    doc_list = []
    for doc in docs:
        doc_list.append({
            'author_names': doc.author_names,
            'title': doc.title,
            'publicationName': doc.publicationName,
            'volume': doc.volume,
            'issueIdentifier': doc.issueIdentifier,
            'pageRange': doc.pageRange,
            'year': doc.coverDate.split('-')[0],
            'coverDate': doc.coverDate,
            'doi': doc.doi,
            'author_ids': doc.author_ids,
            'author_count': doc.author_count,
            'citedby_count': doc.citedby_count,
            'type': doc.subtypeDescription,
        })

    if save_csv:
        df = pd.DataFrame(doc_list)
        outfile = root_path / 'outputs' / f'author{author_id}-docs.csv'
        df.to_csv(outfile, index=False, sep=';')
        print(f'Created .csv file: {outfile.absolute()}')
    return doc_list


def create_pub_list_tex(
        publications,
        template='publication-list.tex',
        include_doi=False,
        include_citations=False,
):
    # Define the directory where the template is stored
    template_dir = root_path / 'templates'
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template)

    context = {
        'include_doi': include_doi,
        'include_citations': include_citations,
        'publications': publications
    }
    rendered_tex = template.render(context)
    print(rendered_tex)

    # Save the rendered LaTeX content to a file
    outfile = root_path / 'outputs' / 'pub-list.tex'
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(rendered_tex)
    print(f'Created .tex file: {outfile.absolute()}')


if __name__ == '__main__':
    # Example author
    author_id = '54987869500'

    # Create a CSV of articles
    docs = get_author_docs(author_id)
    print('Number of documents:', len(docs))
    print('Sample:', docs[0])

    # Create a formatted list of documents using a template
    create_pub_list_tex(docs, template='publication-list.tex', include_doi=True, include_citations=True)
