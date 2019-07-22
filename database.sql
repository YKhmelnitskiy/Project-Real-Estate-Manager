BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sales" (
	"id"	INTEGER NOT NULL,
	"seller"	TEXT,
	"buyer"	TEXT,
	"sold_price"	INTEGER,
	"closing_date"	TEXT,
	"Type"	TEXT,
	"status"	TEXT,
	"address"	TEXT,
	PRIMARY KEY("id")
);
INSERT INTO sales VALUES(1,'Brittany','rob',34200000,'2019-07-18 05:09:00.000000','condo','sold','1234 push ln euclid, ohio');
INSERT INTO sales VALUES(2,'Brittany','howard',140000,'2019-07-16 05:12:00.000000','ranch','awaiting funds','3245 cline rd cleveland ohio');
INSERT INTO sales VALUES(3,'gsd','bdf',57574,'2019-07-04 10:31:00.000000','condo','sold','r2r2r2fwfve');
INSERT INTO sales VALUES(4,'dfds','dfdas',3453242,'2019-07-18 03:34:00.000000','dfds','dfds','dfds');
INSERT INTO sales VALUES(5,'','eikka',234223,'2019-07-01 01:31:00.000000','fsdfs','sold','fsdssdcwefw');
COMMIT;
