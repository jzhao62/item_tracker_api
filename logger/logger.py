import logging
from logdna import LogDNAHandler
from config.settings import INGESTION_KEY


def log(data, handler_name):
    log = logging.getLogger('logdna')
    log.setLevel(logging.INFO)

    options = {'hostname': 'Leetcode_API', 'index_meta': True}

    # Defaults to False; when True meta objects are searchable
    log.addHandler(LogDNAHandler(INGESTION_KEY, options))

    meta = {
        "handler_name": handler_name
    }

    opts = {
        'level': 'warn',
        'meta': meta
    }

    log.info(data, opts)

