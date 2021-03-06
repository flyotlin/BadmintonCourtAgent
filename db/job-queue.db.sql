BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "JobDay" (
	"id"	INTEGER NOT NULL UNIQUE,
	"job_id"	INTEGER NOT NULL,
	"day"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("job_id") REFERENCES "Job"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Job" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"hour"	INTEGER NOT NULL,
	"minute"	INTEGER NOT NULL,
	"callback"	TEXT NOT NULL,
	"chat_id"	INTEGER NOT NULL,
	"worker_type"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
