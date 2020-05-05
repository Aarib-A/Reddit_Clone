BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "comments" (
	"owner_id"	INTEGER NOT NULL,
	"post_id"	INTEGER NOT NULL,
	"comment_id"	INTEGER NOT NULL,
	"parent_id"	NUMERIC,
	"upvotes"	INTEGER NOT NULL,
	"downvotes"	INTEGER NOT NULL,
	"karma"	INTEGER,
	"date"	TEXT NOT NULL,
	"comment_body"	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "Posts" (
	"comm_name"	TEXT,
	"Owner_ID"	INTEGER NOT NULL,
	"owner_name"	TEXT NOT NULL,
	"post_id"	INTEGER NOT NULL,
	"post_title"	TEXT,
	"post_body"	TEXT NOT NULL,
	"upvotes"	INTEGER NOT NULL,
	"downvotes"	INTEGER NOT NULL,
	"karma"	INTEGER,
	"date"	TEXT NOT NULL,
	PRIMARY KEY("post_id")
);
CREATE TABLE IF NOT EXISTS "communities" (
	"comm_name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("comm_name")
);
CREATE TABLE IF NOT EXISTS "Owners" (
	"owner_id"	INTEGER NOT NULL UNIQUE,
	"owner_name"	TEXT NOT NULL,
	"password"	TEXT,
	PRIMARY KEY("owner_id")
);
INSERT INTO "comments" ("owner_id","post_id","comment_id","parent_id","upvotes","downvotes","karma","date","comment_body") VALUES (124578,1200,134679,NULL,1,0,1,'2020-03-09 19:23:26.603080','I wholly agree. You can''t beat the originals. The orginal modern warfare series were part of my child hood. *exhale*, good times.'),
 (1,1200,258164,134679,1,0,1,'2020-03-09 19:26:41.699580','Ditto');
INSERT INTO "Posts" ("comm_name","Owner_ID","owner_name","post_id","post_title","post_body","upvotes","downvotes","karma","date") VALUES ('weebs',1,'Mike',787,'Why Sheild Hero is good?','BC Raphtalia is best waifu',5,1,4,'2020-03-08 01:54:47.039908'),
 ('gaming',9000,'Just some guy',1200,'Good taste','the original COD:MW is still alot better than the reboot.',3,1,2,'2020-03-08 02:01:35.184508');
INSERT INTO "communities" ("comm_name") VALUES ('weebs'),
 ('gaming');
INSERT INTO "Owners" ("owner_id","owner_name","password") VALUES (1,'Mike','NOTpassword'),
 (9000,'Just some guy','password'),
 (124578,'Nobody_JustNobody','definitelyNOTpassword');
COMMIT;
