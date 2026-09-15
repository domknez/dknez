CREATE TABLE IF NOT EXISTS counters (
  k TEXT PRIMARY KEY,
  n INTEGER NOT NULL DEFAULT 0
);
-- one row per visitor per day; the hash is salted with the date, so it is
-- meaningless after midnight and rows are purged after two days
CREATE TABLE IF NOT EXISTS seen (
  h   TEXT PRIMARY KEY,
  day TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS seen_day ON seen (day);
INSERT OR IGNORE INTO counters (k, n) VALUES ('total', 0);
