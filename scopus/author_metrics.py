from pathlib import Path

import pandas as pd
import pybliometrics
from pybliometrics.scopus import AuthorRetrieval


# File system
file_path = Path(__file__).resolve()
root_path = file_path.parents[1]

# Initialize Scopus API connection
pybliometrics.scopus.init()


def get_author_metrics(author_id: str):
    """
    Get author data object for a given author_id.
    """
    au = AuthorRetrieval(author_id)
    return {
        'name': f"{au.initials} {au.surname}",
        'full_name': f"{au.given_name} {au.surname}",
        'orcid': au.orcid,
        'document_count': au.document_count,
        'cited_by_count': au.cited_by_count,
        'citations_count': au.citation_count,
        'coauthor_count': au.coauthor_count,
        'h_index': au.h_index,
    }


def author_metrics(author_list=None, author_file=None):
    if author_file:
        df = pd.read_csv(author_file)
        author_list = list(df['id'])

    author_data = []
    for id in author_list:
        author_data.append(get_author_metrics(id))

    df = pd.DataFrame(author_data)
    df.insert(0, 'scopus_id', author_list)
    outfile = root_path / 'outputs' / f'author-data-list.csv'
    df.to_csv(outfile, index=False, sep=';')
    print(f'Created .csv file: {outfile.absolute()}')
    return df


if __name__ == '__main__':
    # Print data for author IDs in list
    authors = [
        '54987869500',
        '57195637544'
    ]

    for id in authors:
        author_data = get_author_metrics(id)
        print(author_data)

    # Load Scopus IDs from a CSV file and output data to CSV
    author_metrics(author_list=authors)
    # author_metrics(author_file='../data/author-ids-list.csv')
