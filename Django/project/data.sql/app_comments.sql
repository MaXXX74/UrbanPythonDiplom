PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO app_comments VALUES(1,1,1,'Фильм 1, комментарий 1',1725482668);
INSERT INTO app_comments VALUES(2,1,2,'Фильм 2, комментарий 1',1725482688);
INSERT INTO app_comments VALUES(3,1,1,'Фильм 1, комментарий 2',1725482698);
INSERT INTO app_comments VALUES(4,1,5,'Фильм 5, комментарий 1',1725542120);
INSERT INTO app_comments VALUES(5,1,5,'Фильм 5, комментарий 2',1725542183);
INSERT INTO app_comments VALUES(6,1,5,'Фильм 5, комментарий 3',1725542248);
INSERT INTO app_comments VALUES(7,1,6,'Фильм 6, комментарий 1',1725542268);
INSERT INTO app_comments VALUES(8,1,6,'Фильм 6, комментарий 2',1725542283);
COMMIT;
