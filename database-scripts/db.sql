
create database localaidb;
use localaidb;

create table state(state_id int, state_name varchar(256), usps_state_abbrrevation varchar(256));
ALTER TABLE state ADD CONSTRAINT pk_state PRIMARY KEY (state_id);
insert into state values(1, 'North Dakota', 'ND');
insert into state values(2, 'Minnesota', 'MN');
/* The original project was with a Minnesota newsroom. Add states as needed for your newsroom. */

create table category(category_id int, category_name varchar(256));
ALTER TABLE category ADD CONSTRAINT pk_category PRIMARY KEY (category_id);
insert into category values(1, 'Murder');
insert into category values(2, 'Rape');

select * from category;
insert into category values(3, 'Robbery');
insert into category values(4, 'Aggravated assault');
/* These sample categories are from the FBI's violent crime database. */

create table parser(parser_id int, parser_name varchar(256), parser_script_location varchar(256));
ALTER TABLE parser ADD CONSTRAINT pk_parser PRIMARY KEY (parser_id);
insert into parser values(1, 'Brainerd Format', 'FUTURE_USE_1');
insert into parser values(2, 'Cass County Format', 'FUTURE_USE_2');
/* These parsers are named by the main agency they process for convenience. Other agencies can use the parser, in this case, Baxter Police uses the Brainerd format.
In the future, the python script will need to call this table to identify the location of the parser script. Right now, the parser numbers are hardcoded.
*/

create table agency(agency_id int, agency_name varchar(256), city varchar(254), state_id int, parser_id int);
ALTER TABLE agency ADD CONSTRAINT pk_agency PRIMARY KEY (agency_id);
ALTER TABLE agency ADD CONSTRAINT fk_agency FOREIGN KEY (parser_id) REFERENCES parser (parser_id);
ALTER TABLE agency ADD CONSTRAINT fk2_agency FOREIGN KEY (state_id) REFERENCES state (state_id);
insert into agency values(1, 'Brainerd Police' , 'Brainerd', 2, 1);
insert into agency values(2, 'Cass County Sheriff' , 'Walker', 2, 2);
insert into agency values(3, 'Baxter Police' , 'Baxter', 2, 1);
select * from agency;

create table publication(publication_id int, publication_name varchar(256), city varchar(256), state_id int, vendor_id varchar(256));
ALTER TABLE publication ADD CONSTRAINT pk_publication PRIMARY KEY (publication_id);
ALTER TABLE publication ADD CONSTRAINT fk_publication FOREIGN KEY (state_id) REFERENCES state (state_id);
insert into publication values(1, 'Brainerd Dispatch', 'Brainerd', 2, 'LedeAI');

create table user(user_id int, user_name varchar(256), user_password text, user_firstname varchar(256), user_lastname varchar(256));
ALTER TABLE user ADD CONSTRAINT pk_users PRIMARY KEY (user_id);
insert into user values(1, 'admin', '3a7340e0205ac79ce58281c45739bd66b6600957b102ce8f5c48c33fb90e0f8a4ce2daf3bf16d165a416c9f65d41df356927cb044647db40e670725716a43ba4', 'Admin FN', 'Admin LN');
select * from user;
/* The password is: LoveLocalNews2023! */

create table casedetail(case_id int, case_number varchar(256), case_desc text, category_id int, reported_dt datetime, names_involved text, officers_involved text, agency_id int, latitude decimal, longitude decimal, address_line1 text, city varchar(256), zipcode varchar(256),resoource_id varchar(1000), state_id int, upload_userid int, upload_dt datetime, is_ignored boolean default 0);
select * from casedetail;
ALTER TABLE casedetail ADD CONSTRAINT pk_casedetails PRIMARY KEY (case_id);
ALTER TABLE casedetail ADD CONSTRAINT fk_casedetails FOREIGN KEY (state_id) REFERENCES state (state_id);
ALTER TABLE casedetail ADD CONSTRAINT fk2_casedetails FOREIGN KEY (upload_userid) REFERENCES user (user_id);
ALTER TABLE casedetail ADD CONSTRAINT fk4_casedetails FOREIGN KEY (category_id) REFERENCES category (category_id);
ALTER TABLE casedetail ADD CONSTRAINT fk5_casedetails FOREIGN KEY (agency_id) REFERENCES agency (agency_id);


create table pub_agency(pub_agency_id int, agency_id int, publication_id int);
ALTER TABLE pub_agency ADD CONSTRAINT pk_pub_agency PRIMARY KEY (pub_agency_id);
ALTER TABLE pub_agency ADD CONSTRAINT fk_pub_agency FOREIGN KEY (agency_id) REFERENCES agency (agency_id);
ALTER TABLE pub_agency ADD CONSTRAINT fk2_pub_agency FOREIGN KEY (publication_id) REFERENCES publication (publication_id);


create table priority(priority_id int, publication_id int, category_id int, priority int);
ALTER TABLE priority ADD CONSTRAINT pk_priority PRIMARY KEY (priority_id);
ALTER TABLE priority ADD CONSTRAINT fk_priority FOREIGN KEY (category_id) REFERENCES category (category_id);
ALTER TABLE priority ADD CONSTRAINT fk2_priority FOREIGN KEY (publication_id) REFERENCES publication (publication_id);
insert into priority values(1, 1, 1, 1);
insert into priority values(2, 1, 2, 1);
insert into priority values(3, 1, 3, 1);
insert into priority values(4, 1, 4, 1);

select * from category;
select * from priority;

create table user_pub(user_pub_id int, user_id int, publication_id int);
ALTER TABLE user_pub ADD CONSTRAINT pk_user_pub PRIMARY KEY (user_pub_id);
ALTER TABLE user_pub ADD CONSTRAINT fk_user_pub FOREIGN KEY (user_id) REFERENCES user (user_id);
ALTER TABLE user_pub ADD CONSTRAINT fk2_user_pub FOREIGN KEY (publication_id) REFERENCES publication (publication_id);
insert into user_pub values(1, 1, 1);


create table parse_col_map(pcm_id int, parser_id int , agency_id int, parser_colname varchar(256), db_colname varchar(256));
ALTER TABLE parse_col_map ADD CONSTRAINT pk_parse_col_map PRIMARY KEY (pcm_id);
ALTER TABLE parse_col_map ADD CONSTRAINT fk_parse_col_map FOREIGN KEY (parser_id) REFERENCES parser (parser_id);
ALTER TABLE parse_col_map ADD CONSTRAINT fk_parse_col_map2 FOREIGN KEY (agency_id) REFERENCES agency (agency_id);
insert into parse_col_map values(1, 1, 1, 'Names Involved', 'Names Involved');
insert into parse_col_map values(2, 1, 1, 'Officers Involved', 'Officers Involved');
insert into parse_col_map values(3, 1, 1, 'Addresses Involved', 'Addresses Involved');
insert into parse_col_map values(4, 1, 1, 'Reported', 'Reported Date');
select * from parse_col_map;
/* These mappings allow for fast updates when the text of a parsed document changes, but its format does not. This supports the future self-service matching feature. */

create table general_settings(gs_id int, gs_name varchar(256), gs_value text);
ALTER TABLE general_settings ADD CONSTRAINT pk_general_settings PRIMARY KEY (gs_id);
insert into general_settings values(1, 'VENDOR_URI', 'LEDE_AI_API_URI');
insert into general_settings values(2, 'STAGING_LOCATION', '/home/ubuntu/brainerd/staging');
select * from general_settings;


create table report(report_id int, report_dt datetime, report_created_by_userid int, publication_id int, case_id int, report_sent_to_vender boolean, report_sent_dt datetime, report_sent_by_userid int);
ALTER TABLE report ADD CONSTRAINT pk_report PRIMARY KEY (report_id);
ALTER TABLE report ADD CONSTRAINT fk_report FOREIGN KEY (report_created_by_userid) REFERENCES user (user_id);
ALTER TABLE report ADD CONSTRAINT fk2_report FOREIGN KEY (publication_id) REFERENCES publication (publication_id);
ALTER TABLE report ADD CONSTRAINT fk3_report FOREIGN KEY (case_id) REFERENCES casedetail (case_id);
ALTER TABLE report ADD CONSTRAINT fk4_report FOREIGN KEY (report_sent_by_userid) REFERENCES user (user_id);





