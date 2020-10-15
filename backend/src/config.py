from pathlib import Path

COMMENTS_FILE = Path.cwd() / 'comments.csv'
INDEX_FILE = lambda space: Path.cwd() / f'ann_index_{space}'
