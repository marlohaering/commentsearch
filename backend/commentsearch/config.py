from pathlib import Path

WORK_DIR = Path.cwd() / 'work'
COMMENTS_FILE = WORK_DIR / 'comments.csv'
INDEX_FILE = lambda space: WORK_DIR / f'ann_index_{space}'
