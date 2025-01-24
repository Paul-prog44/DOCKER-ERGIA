DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS statuses CASCADE;
DROP TABLE IF EXISTS original_texts CASCADE; 
DROP TABLE IF EXISTS summaries CASCADE;
DROP TABLE IF EXISTS annotations CASCADE;
DROP TABLE IF EXISTS scus CASCADE;
DROP TABLE IF EXISTS campaigns_users CASCADE;
DROP TABLE IF EXISTS original_texts_summaries CASCADE;

CREATE TABLE "users" (
  "id_user" SERIAL PRIMARY KEY,
  "lastname" varchar(30),
  "firstname" varchar(30),
  "email" varchar(50),
  "password" varchar,
  "accept_cgu" boolean
);

CREATE TABLE "campaigns" (
  "id_campaign" SERIAL PRIMARY KEY,
  "name" varchar(50),
  "owner_id" int,
  "status_id" int,
  "creation_date" date,
  "date_phase_1" date,
  "date_phase_2" date
);

CREATE TABLE "statuses" (
  "id_status" SERIAL PRIMARY KEY,
  "name" varchar(30)
);

CREATE TABLE "original_texts" (
  "id_original_text" SERIAL PRIMARY KEY,
  "path" varchar(100),
  "campaign_id" int
);

CREATE TABLE "summaries" (
  "id_summary" SERIAL PRIMARY KEY,
  "path" varchar(100),
  "original_text_id" int,
  "annotator_id" int,
  "ia_generated" boolean
);

CREATE TABLE "annotations" (
  "id_annotation" SERIAL PRIMARY KEY,
  "scu_id" int,
  "color" varchar(20),
  "summary_id" int,
  "index" int,
  "length" int,
  "creator" int
);

CREATE TABLE "scus" (
  "id_scu" SERIAL PRIMARY KEY,
  "idea" varchar(200),
  "weight" int
);

CREATE TABLE "campaigns_users" (
  "campaigns_id_campaign" int,
  "users_id_user" int,
  PRIMARY KEY ("campaigns_id_campaign", "users_id_user")
);

ALTER TABLE "campaigns_users" ADD FOREIGN KEY ("campaigns_id_campaign") REFERENCES "campaigns" ("id_campaign");

ALTER TABLE "campaigns_users" ADD FOREIGN KEY ("users_id_user") REFERENCES "users" ("id_user");

ALTER TABLE "campaigns" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id_user");

ALTER TABLE "campaigns" ADD FOREIGN KEY ("status_id") REFERENCES "statuses" ("id_status");

ALTER TABLE "original_texts" ADD FOREIGN KEY ("campaign_id") REFERENCES "campaigns" ("id_campaign");

CREATE TABLE "original_texts_summaries" (
  "original_texts_id_original_text" int,
  "summaries_id_summary" int,
  PRIMARY KEY ("original_texts_id_original_text", "summaries_id_summary")
);

ALTER TABLE "summaries" ADD FOREIGN KEY ("annotator_id") REFERENCES "users" ("id_user");

ALTER TABLE "original_texts_summaries" ADD FOREIGN KEY ("original_texts_id_original_text") REFERENCES "original_texts" ("id_original_text");

ALTER TABLE "original_texts_summaries" ADD FOREIGN KEY ("summaries_id_summary") REFERENCES "summaries" ("id_summary");

ALTER TABLE "annotations" ADD FOREIGN KEY ("scu_id") REFERENCES "scus" ("id_scu");

ALTER TABLE "annotations" ADD FOREIGN KEY ("summary_id") REFERENCES "summaries" ("id_summary");

ALTER TABLE "annotations" ADD FOREIGN KEY ("creator") REFERENCES "users" ("id_user");

-- INSERTION DES DONNÉES

INSERT INTO "users" (lastname, firstname, email, password, accept_cgu) VALUES
('Musk', 'Elon', 'elon.musk@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Doe', 'Jane', 'jane.doe@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Smith', 'John', 'john.smith@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Brown', 'Alice', 'alice.brown@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Davis', 'Bob', 'bob.davis@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Taylor', 'Emma', 'emma.taylor@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Anderson', 'Eve', 'eve.anderson@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Moore', 'Chris', 'chris.moore@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Clark', 'Sophia', 'sophia.clark@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE),
('Harris', 'James', 'james.harris@example.com', 'a109e36947ad56de1dca1cc49f0ef8ac9ad9a7b1aa0df41fb3c4cb73c1ff01ea', TRUE);


INSERT INTO "statuses" (name) VALUES
('Active'),
('Inactive'),
('Pending'),
('Completed'),
('Cancelled'),
('Phase1Active'),
('Phase1Close'),
('Phase2Active'),
('Phase2Close');

INSERT INTO "campaigns" (name, owner_id, status_id, creation_date, date_phase_1, date_phase_2) VALUES
('Tech for Good', 2, 1, '2024-03-15', '2024-04-15', '2024-05-15'),
('Green Future', 3, 2, '2024-04-01', '2024-05-01', '2024-06-01'),
('AI Revolution', 4, 3, '2024-05-10', '2024-06-10', '2024-07-10'),
('Space Exploration', 5, 4, '2024-06-01', '2024-07-01', '2024-08-01'),
('Next-Gen Energy', 1, 5, '2024-07-15', '2024-08-15', '2024-09-15'),
('Smart Cities Initiative', 2, 1, '2024-08-01', '2024-09-01', '2024-10-01'),
('Clean Water Project', 3, 2, '2024-09-10', '2024-10-10', '2024-11-10'),
('Education for All', 4, 3, '2024-10-01', '2024-11-01', '2024-12-01'),
('Sustainable Farming', 5, 4, '2024-11-15', '2024-12-15', '2025-01-15');

INSERT INTO "original_texts" (path, campaign_id) VALUES
('/texts/text1.txt', 1),
('/texts/text2.txt', 2),
('/texts/text3.txt', 3),
('/texts/text4.txt', 4),
('/texts/text5.txt', 5);

INSERT INTO "summaries" (path, original_text_id, annotator_id, ia_generated) VALUES
('/summaries/summary1.txt', 1, 1, TRUE),
('/summaries/summary2.txt', 2, 2, FALSE),
('/summaries/summary3.txt', 3, 3, TRUE),
('/summaries/summary4.txt', 4, 4, FALSE),
('/summaries/summary5.txt', 5, 5, TRUE);

INSERT INTO "scus" (idea, weight) VALUES
('Main idea 1', 3),
('Main idea 2', 5),
('Key point 1', 2),
('Key point 2', 4),
('Supporting fact 1', 1);

INSERT INTO "annotations" (scu_id, color, summary_id, index, length, creator) VALUES
(1, '#FF0000', 1, 0, 10, 1),
(2, '#00FF00', 2, 11, 15, 2),
(3, '#0000FF', 3, 16, 20, 3),
(4, '#FFFF00', 4, 21, 25, 4),
(5, '#FF00FF', 5, 26, 30, 5);

INSERT INTO "campaigns_users" (campaigns_id_campaign, users_id_user) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO "original_texts_summaries" (original_texts_id_original_text, summaries_id_summary) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
