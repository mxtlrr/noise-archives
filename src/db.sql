CREATE TABLE artist (
  ID          INTEGER       PRIMARY KEY AUTOINCREMENT,
  NAME        TEXT                           NOT NULL, /* Band/artist name */
  FORMED      INTEGER                        NOT NULL, /* Year formed in   */
  SPLITUP     INTEGER,                                 /* (optional) Split up year */
  GENRE       TEXT                           NOT NULL  /* Genre */
);

/* Album */
CREATE TABLE album (
  ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
  ARTIST_NAME INTEGER                      NOT NULL,
  ALBUM_NAME  TEXT                         NOT NULL, /* Album name    */
  YEAR        INTEGER                      NOT NULL  /* Year released */
);
