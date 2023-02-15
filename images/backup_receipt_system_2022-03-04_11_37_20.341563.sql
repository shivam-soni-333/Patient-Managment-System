BEGIN TRANSACTION;
CREATE TABLE "charge" (
	"id"	INTEGER,
	"name"	TEXT,
	"dep_id"	NUMERIC,
	"new_case_fee"	NUMERIC,
	"old_case_fee"	NUMERIC,
	FOREIGN KEY("dep_id") REFERENCES "department"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "charge" VALUES(1,'paracitamol',1,10,10);
INSERT INTO "charge" VALUES(2,'eye drops',2,100,100);
INSERT INTO "charge" VALUES(3,'orient powder',3,300,300);
INSERT INTO "charge" VALUES(4,'loip me',4,20,2);
CREATE TABLE "department" (
	"id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "department" VALUES(1,'general');
INSERT INTO "department" VALUES(2,'eye');
INSERT INTO "department" VALUES(3,'skin');
INSERT INTO "department" VALUES(4,'physiotherapy');
INSERT INTO "department" VALUES(5,'heart');
CREATE TABLE "doctor" (
	"id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "doctor" VALUES(1,'Dr. Jagdish Ahir');
INSERT INTO "doctor" VALUES(2,'Dr. chetan soni');
CREATE TABLE "image" (
	"id"	INTEGER,
	"bg_img"	TEXT,
	"receipt_banner"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "image" VALUES(1,'C:\Users\I MOGAL\Desktop\receipt_system\images\bg.jpg','C:\Users\I MOGAL\Desktop\receipt_system\images\banner.png');
CREATE TABLE "manage_receipt_no" (
	"id"	INTEGER,
	"receipt_no"	INTEGER NOT NULL,
	"year"	TEXT, dept_id REFERENCES department(id),
	FOREIGN KEY("year") REFERENCES "year"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "manage_receipt_no" VALUES(1,3,'1',1);
INSERT INTO "manage_receipt_no" VALUES(2,2,'1',2);
INSERT INTO "manage_receipt_no" VALUES(3,2,'1',3);
INSERT INTO "manage_receipt_no" VALUES(4,2,'1',4);
CREATE TABLE "path_for_saving_receipt" (
	"id"	INTEGER,
	"folderpath"	TEXT,
	PRIMARY KEY("id")
);
INSERT INTO "path_for_saving_receipt" VALUES(1,'C:/Users/I MOGAL/Desktop/receipt_system/saved_receipt');
CREATE TABLE "patient" (
	"id"	INTEGER,
	"name"	TEXT,
	"address"	TEXT,
	"age"	INTEGER,
	"gender"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "patient" VALUES(1,'shivam soni','jamangar',19,'male');
INSERT INTO "patient" VALUES(2,'panaben','jamangar',50,'female');
INSERT INTO "patient" VALUES(3,'tet','test',11,'male');
INSERT INTO "patient" VALUES(4,'rizvanbhai','rajkot',19,'male');
INSERT INTO "patient" VALUES(5,'priyanshpandhi','jamangar',19,'male');
INSERT INTO "patient" VALUES(6,'paragsoni','jamangar',10,'male');
INSERT INTO "patient" VALUES(7,'devanshu padhiyar','ahemdabad',20,'male');
INSERT INTO "patient" VALUES(8,'prem soni','rajkot',20,'male');
INSERT INTO "patient" VALUES(9,'naman shah','rajkot',20,'male');
INSERT INTO "patient" VALUES(10,'KISAN RAMOLIYA','RAJKOT',20,'male');
INSERT INTO "patient" VALUES(11,'TAHER MODI','DUBAI',10,'male');
INSERT INTO "patient" VALUES(12,'shivam soni','jamangar',19,'male');
INSERT INTO "patient" VALUES(13,'priyansh pandhi','jamnagar',20,'male');
INSERT INTO "patient" VALUES(14,'parag soni','jamangar',20,'male');
INSERT INTO "patient" VALUES(15,'rizvan','jamnagar',20,'male');
INSERT INTO "patient" VALUES(16,'devanshu','ahemdabad',19,'male');
CREATE TABLE "receipt" (
	"id"	INTEGER,
	"receipt_no"	INTEGER NOT NULL,
	"pid"	INTEGER,
	"date"	TEXT,
	"doc_name"	TEXT,
	"case_no"	INTEGER,
	"token_no"	INTEGER,
	"pay_method"	TEXT,
	"sub_total"	REAL,
	"discount"	REAL,
	"grand_total"	REAL COLLATE UTF16CI,
	"year"	INTEGER, dept_id REFERENCES department(id),
	FOREIGN KEY("year") REFERENCES "year"("id"),
	FOREIGN KEY("pid") REFERENCES "patient"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "receipt" VALUES(1,1,12,'02/03/2022','Dr. chetan soni',1,2,'CHEQUE',1120.0,20.0,1100.0,1,2);
INSERT INTO "receipt" VALUES(2,1,13,'02/03/2022','Dr. Jagdish Ahir',2,2,'CASH',230.0,0.0,230.0,1,1);
INSERT INTO "receipt" VALUES(3,1,14,'02/03/2022','Dr. Jagdish Ahir',3,4,'CASH',800.0,0.0,800.0,1,4);
INSERT INTO "receipt" VALUES(4,1,15,'02/03/2022','Dr. Shivam Soni',4,5,'POS',600.0,0.0,600.0,1,3);
INSERT INTO "receipt" VALUES(5,2,16,'04/03/2022','Dr. Jagdish Ahir',1,1,'POS',473.0,23.0,450.0,1,1);
CREATE TABLE "receipt_charge" (
	"id"	INTEGER,
	"receipt_id"	INTEGER,
	"name"	TEXT,
	"rate"	INTEGER,
	"no_of_times"	INTEGER,
	"total"	REAL,
	"year"	TEXT,
	FOREIGN KEY("receipt_id") REFERENCES "receipt"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "receipt_charge" VALUES(1,1,'orient powder',300,2,600.0,'1');
INSERT INTO "receipt_charge" VALUES(2,1,'paracitamol',10,2,20.0,'1');
INSERT INTO "receipt_charge" VALUES(3,1,'orient powder',250,2,500.0,'1');
INSERT INTO "receipt_charge" VALUES(4,2,'paracitamol',10,23,230.0,'1');
INSERT INTO "receipt_charge" VALUES(5,3,'orient powder',300,2,600.0,'1');
INSERT INTO "receipt_charge" VALUES(6,3,'paracitamol',10,20,200.0,'1');
INSERT INTO "receipt_charge" VALUES(7,4,'orient powder',300,2,600.0,'1');
INSERT INTO "receipt_charge" VALUES(8,5,'fever',2,2,4.0,'1');
INSERT INTO "receipt_charge" VALUES(9,5,'paracitamol',10.4,23,239.2,'1');
INSERT INTO "receipt_charge" VALUES(10,5,'paracitamol',10,23,230.0,'1');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('charge',4);
INSERT INTO "sqlite_sequence" VALUES('user',1);
INSERT INTO "sqlite_sequence" VALUES('doctor',2);
INSERT INTO "sqlite_sequence" VALUES('department',5);
INSERT INTO "sqlite_sequence" VALUES('token_no',5);
INSERT INTO "sqlite_sequence" VALUES('patient',16);
INSERT INTO "sqlite_sequence" VALUES('year',1);
INSERT INTO "sqlite_sequence" VALUES('manage_receipt_no',4);
INSERT INTO "sqlite_sequence" VALUES('image',1);
INSERT INTO "sqlite_sequence" VALUES('receipt',5);
INSERT INTO "sqlite_sequence" VALUES('receipt_charge',10);
CREATE TABLE "token_no" (
	"id"	INTEGER,
	"date"	TEXT,
	"token_no"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "token_no" VALUES(1,'28/02/2022',2);
INSERT INTO "token_no" VALUES(2,'01/03/2022',11);
INSERT INTO "token_no" VALUES(3,'02/03/2022',5);
INSERT INTO "token_no" VALUES(4,'03/03/2022',1);
INSERT INTO "token_no" VALUES(5,'04/03/2022',2);
CREATE TABLE "user" (
	"id"	INTEGER,
	"username"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "user" VALUES(1,'admin','admin');
CREATE TABLE "year" (
	"id"	INTEGER,
	"start_date"	TEXT,
	"end_date"	TEXT, is_current_year int DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "year" VALUES(1,'01/04/2021','31/03/2022',1);
COMMIT;
