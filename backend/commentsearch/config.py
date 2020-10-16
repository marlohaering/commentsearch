from pathlib import Path

SELECTED_DATA = 'spon'

WORK_DIR = Path.cwd() / 'work'
CSV_SPON_COMMENTS = WORK_DIR / 'comments_spon.csv'
CSV_WHATSAPP_COMMENTS = WORK_DIR / 'comments_whatsapp.csv'
INDEX_FILE = lambda space: WORK_DIR / f'ann_index_{SELECTED_DATA}_{space}'
SQLITE_FILE = WORK_DIR / f'{SELECTED_DATA}_comments.sqlite'
