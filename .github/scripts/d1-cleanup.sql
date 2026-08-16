-- Only remove sessions that have already expired.
-- Adjust the table/column names to your actual schema.

DELETE FROM sessions
WHERE expires_at IS NOT NULL
  AND expires_at < unixepoch();

-- Optional cleanup of explicitly invalidated sessions.
-- Uncomment only if your schema contains this column.
--
-- DELETE FROM sessions
-- WHERE revoked = 1;
