-- Custom text search configuration for domain-specific terminology.

CREATE TEXT SEARCH CONFIGURATION my_config (COPY = english);

-- Custom dictionary for technical terms
CREATE TEXT SEARCH DICTIONARY my_dict (
  TEMPLATE = simple,
  STOPWORDS = english
);

ALTER TEXT SEARCH CONFIGURATION my_config
  ALTER MAPPING FOR asciiword, asciihword
  WITH my_dict, english_stem;

-- Use it like any built-in config:
-- to_tsvector('my_config', title || ' ' || body)
