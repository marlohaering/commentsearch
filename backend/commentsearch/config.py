from pathlib import Path

SELECTED_DATA = 'mast-se-spon'

WORK_DIR = Path.cwd() / 'work'
COMMENTS_CSV_FILE = WORK_DIR / f'comments_{SELECTED_DATA}.csv'
INDEX_FILE = lambda space: WORK_DIR / f'ann_index_{SELECTED_DATA}_{space}'
SQLITE_FILE = WORK_DIR / f'{SELECTED_DATA}_comments.sqlite'

COLIBERT_BATCH_SIZE = 32
