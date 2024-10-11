--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.alembic_version (version_num) VALUES ('51bef700fbf4');


--
-- Data for Name: employee_department; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.employee_department (id, name) VALUES (1, 'Отдел закупок');
INSERT INTO public.employee_department (id, name) VALUES (2, 'Отдел организационно-технической и криптографической защиты информации');
INSERT INTO public.employee_department (id, name) VALUES (3, 'Отдел информационных технологий');
INSERT INTO public.employee_department (id, name) VALUES (4, 'Отдел  установления материнского(семейного) капитала');
INSERT INTO public.employee_department (id, name) VALUES (5, 'Отдел  установления пенсий');


--
-- Data for Name: employee_location_building; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.employee_location_building (id, name, city, street, building, index) VALUES (1, 'Клиентская служба №1', 'Севастополь', 'Урицкого', '2', 92005);
INSERT INTO public.employee_location_building (id, name, city, street, building, index) VALUES (2, 'Клиентская служба №2', 'Севастополь', 'Пожарова', '5', 92002);
INSERT INTO public.employee_location_building (id, name, city, street, building, index) VALUES (3, 'Клиентская служба №3', 'Севастополь', 'Киевская', '11', 92003);
INSERT INTO public.employee_location_building (id, name, city, street, building, index) VALUES (4, 'Отделение', 'Севастополь', 'Музыки', '60А', 92001);
INSERT INTO public.employee_location_building (id, name, city, street, building, index) VALUES (5, 'Управление', 'Севастополь', 'Киевская', '11', 92003);
INSERT INTO public.employee_location_building (id, name, city, street, building, index) VALUES (6, 'Клиентская служба №4', 'Севастополь', 'Музыки', '60А', 92001);


--
-- Data for Name: employee_location; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.employee_location (id, name, building_id) VALUES (1, 'Кабинет №9', 1);
INSERT INTO public.employee_location (id, name, building_id) VALUES (2, 'Кабинет №3', 1);
INSERT INTO public.employee_location (id, name, building_id) VALUES (3, 'Кабинет №20', 4);
INSERT INTO public.employee_location (id, name, building_id) VALUES (5, 'Кабинет №105', 5);
INSERT INTO public.employee_location (id, name, building_id) VALUES (4, 'Кабинет №106', 5);
INSERT INTO public.employee_location (id, name, building_id) VALUES (6, 'Кабинет №214', 5);


--
-- Data for Name: employee_organisation; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.employee_organisation (id, name, short_name, city, street, building, index, chief) VALUES (1, 'Отделение фонда пенсионного и социального страхования РФ по г. Севастополю ', 'ОСФР по г. Севастополю', 'Севастополь', 'Музыки', '60А', 92001, 'Иванов И.И.');


--
-- Data for Name: employee_position; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.employee_position (id, name, is_leadership) VALUES (1, 'Специалист-эксперт', false);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (2, 'Ведущий специалист-эксперт', false);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (3, 'Главный специалист-эксперт', false);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (4, 'Консультант', false);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (5, 'Старший специалист', false);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (6, 'Заместитель начальника отдела', true);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (7, 'Начальник отдела', true);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (8, 'Начальник управления', true);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (9, 'Заместитель начальника управления', true);
INSERT INTO public.employee_position (id, name, is_leadership) VALUES (10, 'Руководитель группы', true);


--
-- Data for Name: employee; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (1, 'Иванов', 'Иван', 'Иванович', true, 1, 1, 1, 1, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (2, 'Петров', 'Петр', 'Петрович', true, 7, 3, 1, 2, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (3, 'Сидоров', 'Сергей', 'Сергеевич', true, 7, 1, 1, 1, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (7, 'Васильева', 'Виктория', 'Валерьевна', true, 1, 4, 1, 4, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (8, 'Тимошенко', 'Ксения', 'Анатольевна', true, 7, 4, 1, 5, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (9, 'Гладунова', 'Юлия', 'Владимировна', true, 1, 4, 1, 4, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (10, 'Самохина', 'Анна', 'Викторовна', true, 7, 5, 1, 6, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (11, 'Дильянова', 'Кристина', 'Намиковна', true, 1, 5, 1, 6, false);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (5, 'Некрасов', 'Александр', 'Борисович', true, 2, 2, 1, 3, true);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (6, 'Чаус', 'Роман', 'Викторович', true, 1, 2, 1, 3, true);
INSERT INTO public.employee (id, surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id, is_security_staff) VALUES (4, 'Данильченко', 'Игорь', 'Владимирович', true, 7, 2, 1, 3, true);


--
-- Data for Name: cryptography_act_record; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (8, 'С_INSTALL', '230220-1', NULL, NULL, '2023-02-20', NULL, NULL, 4, '2024-08-28 07:40:55.854699', '2024-08-28 07:40:55.854699');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (9, 'С_INSTALL', '230216-1', NULL, NULL, '2023-02-16', NULL, NULL, 4, '2024-08-28 08:11:02.317655', '2024-08-28 08:11:02.317655');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (10, 'С_INSTALL', '230216-2', NULL, NULL, '2023-02-16', NULL, NULL, 4, '2024-08-28 08:17:54.072869', '2024-08-28 08:17:54.072869');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (11, 'С_INSTALL', '240404-1', NULL, NULL, '2024-04-04', NULL, NULL, 4, '2024-08-28 08:27:47.412003', '2024-08-28 08:27:47.412003');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (12, 'С_INSTALL', '240404-2', NULL, NULL, '2024-04-04', NULL, NULL, 4, '2024-08-28 08:32:29.580836', '2024-08-28 08:32:29.580836');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (13, 'С_INSTALL', '240422-1', NULL, NULL, '2024-04-22', NULL, NULL, 4, '2024-08-28 09:10:19.556753', '2024-08-28 09:10:19.556753');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (14, 'С_INSTALL', '240422-2', NULL, NULL, '2024-04-22', NULL, NULL, 4, '2024-08-28 09:27:46.469733', '2024-08-28 09:27:46.469733');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (15, 'C_DESTRUCTION', '240903-1', 'Истечение срока действия сертификата соответствия', NULL, '2024-09-03', 4, 6, 5, '2024-09-03 13:58:41.62044', '2024-09-03 13:58:41.62044');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (16, 'C_DESTRUCTION', '240903-2', 'Истечение срока действия сертификата соответствия', NULL, '2024-09-03', 4, 6, 5, '2024-09-03 13:59:22.503904', '2024-09-03 13:59:22.503904');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (21, 'I_INSTALL', '240913-1', 'б\н', '2024-09-12', '2024-09-13', 4, 8, 5, '2024-09-13 11:28:48.586264', '2024-09-13 11:28:48.586264');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (22, 'I_INSTALL', '240917-1', 'б\н', '2024-09-13', '2024-09-17', 4, 8, 5, '2024-09-18 06:01:10.416237', '2024-09-18 06:01:10.416237');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (23, 'I_INSTALL', '240918-1', 'б\н', '2024-09-18', '2024-09-18', 4, 10, 5, '2024-09-18 10:56:30.577205', '2024-09-18 10:56:30.577205');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (24, 'I_INSTALL', '240101-1', 'б\н', '2024-01-01', '2024-01-01', 4, 2, 3, '2024-09-23 12:19:39.187055', '2024-09-23 12:19:39.187055');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (25, 'KD_REMOVE', '240923-1', 'Истечение срока действия', NULL, '2024-09-23', 4, 3, 5, '2024-09-23 13:32:23.28046', '2024-09-23 13:32:23.28046');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (26, 'KD_REMOVE', '240923-2', 'Истечение срока действия', NULL, '2024-09-23', 4, 3, 5, '2024-09-23 13:33:12.685076', '2024-09-23 13:33:12.685076');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (27, 'KD_REMOVE', '240923-3', 'Истечение срока действия', NULL, '2024-09-23', 4, 3, 5, '2024-09-23 13:34:43.583563', '2024-09-23 13:34:43.583563');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (46, 'I_INSTALL', '240101-2', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-24 13:20:11.202838', '2024-09-24 13:20:11.202838');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (47, 'KD_REMOVE', '240924-1', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-24 13:20:12.602597', '2024-09-24 13:20:12.602597');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (1, 'I_INSTALL', '240101-3', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-25 14:35:43.389213', '2024-09-25 14:35:43.389213');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (2, 'I_INSTALL', '240101-4', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-25 14:37:27.208946', '2024-09-25 14:37:27.208946');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (3, 'KD_REMOVE', '240924-2', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-25 15:01:05.567049', '2024-09-25 15:01:05.567049');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (4, 'I_INSTALL', '240101-5', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 07:32:20.464338', '2024-09-27 07:32:20.464338');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (49, 'I_INSTALL', '240101-6', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 07:45:19.028886', '2024-09-27 07:45:19.028886');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (50, 'KD_REMOVE', '240924-3', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 07:45:56.38196', '2024-09-27 07:45:56.38196');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (51, 'I_INSTALL', '240101-7', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 08:25:46.900964', '2024-09-27 08:25:46.900964');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (52, 'I_INSTALL', '240101-8', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 08:28:09.434337', '2024-09-27 08:28:09.434337');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (53, 'KD_REMOVE', '240924-4', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 08:36:24.880983', '2024-09-27 08:36:24.880983');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (54, 'KD_REMOVE', '240924-5', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 08:39:46.038367', '2024-09-27 08:39:46.038367');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (55, 'KD_REMOVE', '240924-6', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 08:41:15.278044', '2024-09-27 08:41:15.278044');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (56, 'KD_REMOVE', '240924-7', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 09:00:07.392405', '2024-09-27 09:00:07.392405');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (57, 'KD_REMOVE', '240924-8', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 09:01:17.378262', '2024-09-27 09:01:17.378262');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (58, 'I_INSTALL', '240101-9', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 09:07:36.859998', '2024-09-27 09:07:36.859998');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (59, 'KD_REMOVE', '240924-9', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 09:07:59.221709', '2024-09-27 09:07:59.221709');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (60, 'I_INSTALL', '240101-10', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 09:34:49.502536', '2024-09-27 09:34:49.502536');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (61, 'KD_REMOVE', '240924-10', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-27 09:35:15.584592', '2024-09-27 09:35:15.584592');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (62, 'I_INSTALL', '240101-11', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-27 09:48:36.882662', '2024-09-27 09:48:36.882662');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (63, 'KD_REMOVE', '240924-11', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:12:18.612242', '2024-09-30 08:12:18.612242');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (64, 'KD_REMOVE', '240924-12', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:16:47.025804', '2024-09-30 08:16:47.025804');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (65, 'I_INSTALL', '240101-12', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-30 08:22:44.019636', '2024-09-30 08:22:44.019636');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (66, 'KD_REMOVE', '240924-13', 'б\н', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:23:15.54243', '2024-09-30 08:23:15.54243');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (67, 'KD_REMOVE', '240924-14', 'б\н', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:30:36.432222', '2024-09-30 08:30:36.432222');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (68, 'I_INSTALL', '240101-13', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-30 08:31:55.723925', '2024-09-30 08:31:55.723925');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (69, 'KD_REMOVE', '240924-15', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:32:17.004929', '2024-09-30 08:32:17.004929');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (70, 'KD_REMOVE', '240924-16', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:36:38.990043', '2024-09-30 08:36:38.990043');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (71, 'I_INSTALL', '240101-14', 'б\н', '2024-01-01', '2024-01-01', 4, 3, 5, '2024-09-30 08:38:23.485515', '2024-09-30 08:38:23.485515');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (72, 'KD_REMOVE', '240924-17', 'Истечение срока действия', NULL, '2024-09-24', 4, 6, 5, '2024-09-30 08:38:46.409708', '2024-09-30 08:38:46.409708');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (73, 'I_INSTALL', '240930-1', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 08:42:15.488464', '2024-09-30 08:42:15.488464');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (74, 'KD_REMOVE', '240930-2', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 08:42:30.579461', '2024-09-30 08:42:30.579461');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (75, 'KD_REMOVE', '240930-3', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 08:45:51.957703', '2024-09-30 08:45:51.957703');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (76, 'KD_REMOVE', '240930-4', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 08:46:06.040636', '2024-09-30 08:46:06.040636');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (77, 'I_INSTALL', '240930-5', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 08:53:23.353491', '2024-09-30 08:53:23.353491');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (78, 'KD_REMOVE', '240930-6', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 08:53:44.799936', '2024-09-30 08:53:44.799936');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (79, 'KD_REMOVE', '240930-7', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 08:55:41.873711', '2024-09-30 08:55:41.873711');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (80, 'I_INSTALL', '240930-8', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 08:56:37.367135', '2024-09-30 08:56:37.367135');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (81, 'KD_REMOVE', '240930-9', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 08:56:54.250365', '2024-09-30 08:56:54.250365');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (82, 'I_INSTALL', '240930-10', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 09:02:32.656106', '2024-09-30 09:02:32.656106');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (83, 'KD_REMOVE', '240930-11', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 09:02:50.560087', '2024-09-30 09:02:50.560087');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (84, 'I_INSTALL', '240930-12', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 09:05:42.248568', '2024-09-30 09:05:42.248568');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (85, 'KD_REMOVE', '240930-13', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 09:05:59.457598', '2024-09-30 09:05:59.457598');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (86, 'KD_REMOVE', '240930-14', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 09:07:09.602423', '2024-09-30 09:07:09.602423');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (87, 'I_INSTALL', '240930-15', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 09:16:03.248452', '2024-09-30 09:16:03.248452');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (88, 'KD_REMOVE', '240930-16', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 09:16:26.929903', '2024-09-30 09:16:26.929903');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (89, 'I_INSTALL', '240930-17', 'б\н', '2024-09-30', '2024-09-30', 4, 3, 5, '2024-09-30 09:25:55.058128', '2024-09-30 09:25:55.058128');
INSERT INTO public.cryptography_act_record (id, action_type, number, reason, reason_date, happened_at, head_commision_member_id, commision_member_id, performer_id, created_at, updated_at) VALUES (90, 'KD_REMOVE', '240930-18', 'Истечение срока действия', NULL, '2024-09-30', 4, 6, 5, '2024-09-30 09:26:11.993877', '2024-09-30 09:26:11.993877');


--
-- Data for Name: cryptography_key_carrier_type; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (1, 'Чип');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (2, 'Смарт-карта');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (3, 'ОТР-токен');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (4, 'Рутокен S');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (5, 'eToken');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (6, 'USB носитель');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (7, 'SIM-карта');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (8, 'MicroSD-карта');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (9, 'JaCarta PKI/ГОСТ');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (10, 'Контейнер');
INSERT INTO public.cryptography_key_carrier_type (id, name) VALUES (11, 'dst-файл');


--
-- Data for Name: cryptography_key_carrier; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_key_carrier (id, serial, carrier_type_id) VALUES (1, 'ViPNet PKI Client', 10);
INSERT INTO public.cryptography_key_carrier (id, serial, carrier_type_id) VALUES (2, '079C73BE', 9);
INSERT INTO public.cryptography_key_carrier (id, serial, carrier_type_id) VALUES (3, 'Дистрибутив ключей ViPNet', 11);


--
-- Data for Name: cryptography_manufacturer; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_manufacturer (id, name) VALUES (1, 'АО «ИнфоТеКС»');
INSERT INTO public.cryptography_manufacturer (id, name) VALUES (2, 'ООО «КриптоПро»');


--
-- Data for Name: cryptography_model; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_model (id, name, description, type, manufacturer_id) VALUES (2, 'КриптоПро CSP', '- Формирование и проверка электронной подписи.
- Обеспечение конфиденциальности и контроля целостности информации посредством ее шифрования и имитозащиты.
- Обеспечение аутентичности, конфиденциальности и имитозащиты соединений по протоколам TLS, и IPsec.
- Контроль целостности системного и прикладного программного обеспечения для его защиты от несанкционированных изменений и нарушений доверенного функционирования.', 'PROGRAM', 2);
INSERT INTO public.cryptography_model (id, name, description, type, manufacturer_id) VALUES (3, 'ViPNet CSP', '- Создание ключей электронной подписи, формирование и проверка ЭП по ГОСТ Р 34.10-2012.
- Хэширование данных по ГОСТ Р 34.11-2012
- Шифрование и осуществление имитозащиты данных по ГОСТ 28147-89, ГОСТ 34.12-2018, ГОСТ 34.13-2018
- Создание защищенных TLS-соединения (только для Windows)
- Формирование CMS-сообщений, включая расширение CAdES-BES;
- Формирование транспортных ключевых контейнеров.', 'PROGRAM', 1);
INSERT INTO public.cryptography_model (id, name, description, type, manufacturer_id) VALUES (1, 'ViPNet Client', '- VPN-клиент (шифрование и имитозащита IP-пакетов).
- Персональный сетевой экран (в версии ViPNet Client for Windows).
- Контроль сетевой активности приложений и компонентов операционной системы.
- ViPNet Client работает в составе сети ViPNet и совместим со всеми продуктами линейки ViPNet Network Security.', 'PROGRAM', 1);
INSERT INTO public.cryptography_model (id, name, description, type, manufacturer_id) VALUES (4, 'ViPNet PKI Client', '', 'PROGRAM', 1);
INSERT INTO public.cryptography_model (id, name, description, type, manufacturer_id) VALUES (5, 'ViPNet Administrator', '', 'PROGRAM', 1);


--
-- Data for Name: cryptography_version; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (32, '1.x (исп.3)', 'KC3', '905C-008996', 'PKI CI КС3-007996', 'СФ/124-4250', '2025-04-08', 'СФР ЦА', '18-18/25920', '2023-02-20', 'ФРКЕ.00175-02 30 01', '', 4, 4, '2024-08-28 07:40:55.813533', '2024-08-28 09:35:33.784914');
INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (33, '4.4.2 (исп.3)', 'KC3', '637Д-003564', 'CSP4.4исп3-184420', 'СФ/124-4103', '2024-08-10', 'СФР ЦА', '18-18/23986', '2023-02-16', 'ФРКЕ.00106-07 30 01', '', 3, 4, '2024-08-28 07:55:47.556627', '2024-08-28 09:47:32.728379');
INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (34, '4.x', 'KC3', '734A-011337', 'АдКС3-4-3974', 'СФ/124-4225', '2023-12-31', 'СФР ЦА', '18-18/23986', '2023-02-16', 'ФРКЕ.00109-07 30 01 ФО', '', 5, 4, '2024-08-28 08:14:47.841088', '2024-08-28 09:47:38.153033');
INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (36, '4.6.11', 'KC3', '734A-013334', 'АдКС3-013334', 'СФ/124-4701', '2026-12-28', 'СФР', 'АШ 18-18/15289', '2024-04-04', 'ФРКЕ.00109-08 30 01 ФО', 'Бессрочная лицензия на право использования ПО ViPNet Administrator 4.x (КС3)', 5, 4, '2024-08-28 08:27:47.462489', '2024-08-28 09:47:42.842986');
INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (35, '4.4.8 (исп.3)', 'KC3', 'CSP4.4исп3-186614', '637Д-100747', 'СФ/124-4702', NULL, 'СФР', 'АШ 18-18/15289', '2024-04-04', 'ФРКЕ.00106-09 30 01 ФО', '', 3, 4, '2024-08-28 08:17:54.123024', '2024-08-28 09:47:46.498666');
INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (37, '4.5.3.65117 (исп.2)', 'KC2', '782-322249', 'КлКС2-4-321274', 'СФ/124-4778', '2026-02-28', 'СФР', 'АШ 18-18/15289', '2024-04-04', 'ФРКЕ.00116-05 30 01 ФО', '', 1, 4, '2024-08-28 08:59:23.522209', '2024-08-28 09:48:21.200133');
INSERT INTO public.cryptography_version (id, version, grade, serial, dist_num, certificate, certificate_expired_at, received_from, received_num, received_at, form, license, model_id, responsible_user_id, created_at, updated_at) VALUES (38, '4.4.4 (исп.5)', 'KC2', '637Д-100490', 'CSP4.4 исп5-186357', 'СФ/124-4368', '2025-11-08', 'СФР', 'АШ 18-18/15289', '2024-04-04', 'ФРКЕ.00106-08 30 01 ФО', '', 3, 4, '2024-08-28 09:10:19.643189', '2024-09-03 13:46:53.785324');


--
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000332', 'PC00MZTU', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000384', 'PC00NPRS', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000333', 'PC00NM4Q', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000324', 'PC00NMGD', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000146', 'S4Q89144', 'Intel(R) Celeron(R) CPU G1840 @ 2.80GHz ,10 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000353', 'PC00NMBE', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000403', '380872-007', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000367', 'PC00NNUG', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000357', 'PC00MZN0', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000143', 'S4Q89265', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000383', 'PC00NPJ2', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000015', 'PC00MZNT', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000011', 'PC00MXZN', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000386', 'PC00MX13', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000351', 'PC00MY3S', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000331', 'PC00MZRG', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000144', 'S4Q89299', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000335', 'PC00MY4H', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000041', '0', 'Intel Celeron 2.7GHz, 2, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000020', 'PC00NM4F', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000142', 'S4Q89095', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000409', '380872-010', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000401', '380872-012', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000073', 'PB0V3EK', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000074', 'PB0V3EY', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000336', 'PC00MWXN', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000017', 'PC00NNJ3', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000154', 'S4Q89258', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000003', 'DAN0CV031022406', 'ASUS X550L, 15.6, Intel Core i3-4010U 1.7GHz, 6, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000147', 'S4Q89106', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000002', 'DAN0CV03089440F', 'ASUS X550L, 15.6, Intel Core i3-4010U 1.7GHz, 6, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000001', 'DAN0CV030901407', 'ASUS X550L, 15.6, Intel Core i3-4010U 1.7GHz, 6, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000381', 'PC00MZN3', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000330', 'PC00MWWH', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000071', 'PB0V3EX', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000385', 'PC00NPUJ', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000016', 'PC00MY4Z', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000023', 'PC00LTT8', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000359', 'PC00MZN1', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000151', 'S4Q89301', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000022', 'PC00NM4G', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000387', 'PC00NMAQ', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000024', 'PC00NMBM', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000021', 'PC00NMB1', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000358', 'PC00MZMF', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600060', '2141203892017-0061', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140995', '11514935', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141000', '11514938', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000402', '380872-011', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000152', 'S4Q89277', 'Intel(R) Celeron(R) CPU G1820 @ 2.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000072', 'PB0V3EH', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000018', 'PC00MZSQ', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000320', 'PC00MY2S', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000388', 'PC00MZNX', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000361', 'PC00NM4K', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000372', 'PC00MZMZ', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000360', 'PC00MZN2', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000145', 'S4Q89098', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000153', 'S4Q89122', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000043', '1', 'Celeron, 4Gb, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000045', '5,00E+11', 'Celeron, 4Gb, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000042', '3', 'Intel Celeron 2.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000155', 'S4Q89139', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000321', 'PC00MXQY', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000027', '2', 'Intel Pentium G3250 3.20 GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000148', 'S4Q89130', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000337', 'PC00MWZY', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000044', '6', 'Intel(R) Celeron(R) CPU G1620 @ 2.7 GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600011', '2141203892017-0397', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.15.000.0003', '1111', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000638', '2141203892017-0385', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600065', '2141203892001-0141', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.15.000.0002', '1109', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600068', '2141203892017-0009', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,250', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000365', 'PC00MXTU', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000191', '11489106', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140847', '11489346', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000376', 'PC00NMAT', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140139', '2141203892001-0091', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140252', '2141203892017-0367', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140243', '2141203892017-0262', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140286', '2141203892001-0027', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000565', '1105', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000564', '1106', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600018', '2141203892017-0436', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000602', '2141203892017-0563', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140248', '2141203892017-0417', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000380', 'PC00MWWJ', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000382', 'PC00NNG7', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000281', 'R9-0B087X', 'Lenovo ThinkPad L440, 14, Intel Core i5-4300M 2.6-3.3GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140278', '2141203892001-0121', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000366', 'PC00MZNV', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140196', '2141203892001-0214', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140157', '2141203892001-0220', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000555', '11514950', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000190', '11489105', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140208', '2141203892017-0460', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600055', '2141203892017-0363', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000876', '11489004', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140161', '2141203892001-0119', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140215', '2141203892001-0079', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140269', '2141203892001-0173', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140128', '2141203892017-0602', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000518', '9030043', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140866', '2141105830606-0038', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000551', '2141105830606-0011', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140869', '2141105830606-0010', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,12 ,2000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140865', '2141105830606-0028', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000655', '2141203892001-0021', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600050', '2141203892017-0406', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000672', '2141203892017-0352', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000647', '2141203892017-0610', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000594', '2141203892017-0611', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140171', '2141203892017-0386', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000639', '2141203892017-0243', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000617', '2141203892017-0424', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000566', '11514932', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140182', '2141203892001-0093', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140277', '2141203892001-0138', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000643', '2141203892017-0447', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140187', '2141203892017-0498', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140830', '11514947', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000589', '2141203892017-0106', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000596', '2141203892017-0573', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140227', '2141203892017-0522', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140193', '2141203892017-0392', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140127', '2141126892014-0101', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600000008', '10893994', 'Intel(R) Core(TM)2 Duo CPU���� E8400� @ 3.00GHz ,4 ,250', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140136', '2141203892017-0565', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320262015000000001', '10894131', 'Intel(R) Core(TM)2 Duo CPU���� E8400� @ 3.00GHz, 4, 250', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600032', '2141203892017-0036', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600017', '2141203892017-0233', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,250', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600053', '2141203892017-0532', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140845', '11489103', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600041', '2141203892017-0371', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140871', '2141105830606-0050', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000552', '2141105830601-0011', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140544', '2141105830606-0023', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000667', '2141126892014-0013', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000150', 'S4Q89116', 'Intel(R) Core(TM) i3-4150 CPU @ 3.50GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620140000505', '11529196', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140579', 'NXMPGER009513077E86600', 'Acer Aspire V3-371-31C2, 13.3, Intel Core i3 4005U 1.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000645', '2141203892001-0209', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140985', '11529189', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000586', '2141203892001-0043', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140257', '2141126892014-0076', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000651', '2141203892001-0136', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000580', '2141203892017-0305', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000615', '2141203892001-0061', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000189', '11488909', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000681', '2141203892001-0035', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000019', 'PC00NNFP', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000629', '2141203892017-0176', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620140000503', '11514936', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000653', '2141126892014-0086', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430205450009', '11514929', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000377', 'PC00NM8H', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000556', '11514952', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620140000502', '11514942', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000600', '2141203892001-0115', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140843', '11489297', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000610', '2141203892017-0591', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000663', '2141203892017-0484', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000665', '2141203892017-0361', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000676', '2141203892017-0486', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000608', '2141203892017-0479', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000611', '2141203892017-0560', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000578', '2141203892017-0470', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000584', '2141203892001-0129', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000679', '2141203892001-0037', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000598', '2141203892001-0154', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141003', '11514951', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140875', '11489202', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000659', '2141203892017-0619', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140291', '2141203892017-0476', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000625', '2141203892001-0131', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140225', '2141203892001-0005', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000005', '11489154', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000633', '2141203892017-0432', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000592', '2141203892001-0156', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000614', '2141203892017-0380', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000582', '2141203892017-0415', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600054', '2141203892017-0162', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600044', '2141203892017-0375', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600047', '2141203892017-0309', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140984', '11514939', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600000006', '10894091', 'Intel(R) Core(TM)2 Duo CPU���� E8400� @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600070', '2141203892017-0074', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600061', '2141203892001-0155', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,250', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600042', '2141203892017-0540', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600043', '2141203892017-0265', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000588', '2141203892017-0004', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600034', '2141203892017-0024', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140135', '2141203892017-0253', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000684', '2141203892017-0557', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600031', '2141203892001-0230', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140993', '11514943', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140180', '2141126892014-0039', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000669', '2141203892017-0512', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140581', 'NXMPGER0095130781B6600', 'Acer Aspire V3-371-31C2, 13.3, Intel Core i3 4005U 1.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000621', '2141203892017-0210', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140197', '2141203892001-0160', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141002', '11514926', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140835', '11489298', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140288', '2141203892017-0647', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140990', '11529200', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140195', '2141203892017-0098', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140245', '2141203892017-0575', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140126', '2141203892001-0026', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000604', '2141203892001-0095', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140164', '2141203892017-0132', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140117', '2141203892017-0206', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140212', '2141203892017-0552', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140836', '11489194', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140819', '11489225', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140162', '2141203892017-0495', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140140', '2141203892017-0093', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140201', '2141203892017-0496', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141001', '11514927', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140851', '11489274', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000674', '2141203892001-0057', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000558', '11529194', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000877', '11488920', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000025', 'PC00NM4P', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140996', '11514934', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140831', '11489183', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600062', '2141203892001-0120', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140124', '2141203892017-0054', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600049', '2141203892017-0014', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000686', '2141203892017-0526', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000649', '2141203892017-0633', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140141', '2141203892001-0104', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140133', '2141203892001-0228', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140192', '2141203892017-0558', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.150000006', '1101', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140982', '11528658', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600066', '2141203892017-0067', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140146', '2141203892017-0419', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140167', '2141203892017-0341', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140217', '2141203892017-0365', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140170', '2141203892017-0514', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140148', '2141203892017-0605', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140247', '2141203892001-0020', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140786', '11489056', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140279', '2141203892017-0300', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140138', '2141203892017-0359', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140980', '11514948', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140849', '11489185', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140280', '2141203892017-0351', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140994', '11514945', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140143', '2141203892017-0275', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000354', 'PC00NMBL', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000370', 'PC00NM4N', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000363', 'PC00NMB0', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140144', '2141203892017-0261', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000322', 'PC00NMA3', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.150000005', '1107', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000406', '380872-014', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000364', 'PC00MY52', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140284', '2141203892017-0181', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000635', '2141126892014-0017', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000619', '2141126892014-0019', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140176', '2141203892017-0600', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140134', '2141126892014-0075', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140846', '11489168', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000003', 'NXMPGER009513078006600', 'Acer Aspire V3-371-31C2, 13.3, Intel Core i3 4005U 1.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140272', '2141203892001-0089', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140216', '2141203892001-0050', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140118', '2141203892001-0227', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140186', '2141203892017-0073', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000561', '9029709', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140261', '2141203892001-0200', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140229', '2141203892017-0134', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140166', '2141203892001-0167', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140122', '2141203892017-0209', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140121', '2141203892017-0335', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140220', '2141126892014-0083', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140165', '2141203892017-0537', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140156', '2141203892017-0159', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140151', '2141203892001-0201', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140112', '2141203892017-0394', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000501', '10893997', 'Intel(R) Core(TM)2 Duo CPU���� E8400� @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140986', '11514930', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000408', '380872-009', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000521', '9029666', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000560', '9029907', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000536', '9030072', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140131', '2141203892017-0469', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600028', '2141203892017-0886', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000352', 'PC00NNLU', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600030', '2141203892017-0013', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000001', 'R9-0AKVHL', 'Lenovo ThinkPad L540, 14, Intel Core i5-4300M 2.6-3.3GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600029', '2141203892017-0070', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600027', '2141203892017-0410', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000008', '11489065', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000069', 'PB0V3EL', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000371', 'PC00NPVT', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000627', '2141203892001-0011', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140184', '2141203892001-0205', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.150000002', '1110', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140262', '2141203892017-0260', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000369', 'PC00LTSC', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000554', '11514949', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.15.000.0017', '1,00E+12', 'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz, 8, 1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600013', '2141203892001-0084', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140244', '2141203892017-0185', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000046', '10361240', 'Intel Pentium G860 @ 3.0 GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600048', '2141203892017-0409', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600025', '2141203892017-0235', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000010', '11489197', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600022', '2141203892017-0234', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600023', '2141203892001-0074', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140207', '2141203892017-0327', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000009', '11489158', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000015', '5CD6447MGW', 'HP ProBook 430, 13.3, Intel Core i5 7200U 2.5GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600056', '2141203892017-0191', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600063', '2141203892017-0458', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140838', '11489011', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600033', '2141203892017-0310', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000606', '2141203892017-0446', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600024', '2141203892017-0241', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140253', '2141203892017-0281', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000559', '1108', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000156', 'S4Q89107', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140981', '11529260', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000411', '380872-002', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000405', '380872-003', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000410', '380872-004', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000412', '380872-015', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000413', '380872-020', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000504', '10894075', 'Intel(R) Core(TM)2 Duo CPU���� E8400� @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600045', '2141128892014-0021', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140992', '11529195', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600008', '2141105830608-0001', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.150000007', '1102', 'Intel(R) Core(TM) i5-4430 CPU @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000057', '13460/2-7', 'Intel Pentium G860 @ 3.0 GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000004', '11489302', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141009', '11514955', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620111100005', '5CD039MDGW', 'HP 15s-eq0053ur, 15.6, AMD Ryzen 5 3500U, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620111100006', '5CD039MDHP', 'HP 15s-eq0053ur, 15.6, AMD Ryzen 5 3500U, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000041', '11258669', 'Intel(R) Core(TM) i3-3250 CPU @ 3.50GHz ,8 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000553', '2141105830606-0044', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,16 ,750', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600019', '2141203892017-0405', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600035', '2141203892017-0075', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000006', '11489121', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600058', '2141203892017-0500', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000641', '2141203892017-0139', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140840', '11489151', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600009', '2141105830606-0016', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600057', '2141203892017-0008', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000379', 'PC00MZTP', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600039', '2141203892017-0551', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000319', 'PC00MX1A', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600015', '2141203892017-0556', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600051', '2141203892001-0023', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34320.26.20.15.000.0018', '7', 'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz, 8, 1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600052', '2141203892017-0071', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600001', '2141105830601-0008', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202010003', 'MP06FA6M', 'Lenovo ThinkPad Yog S1, 13.3, Intel Core i5-4200U 1.60GHz, 8, 128', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600006', '2141105830606-0009', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600007', '2141105830606-0014', 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600026', '2141203892017-0330', 'Intel(R) Core(TM) i3-3250 CPU @ 3.50GHz ,8 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000607', '2141126892014-0018', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000011', '11489166', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140271', '2141203892001-0232', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600059', '2141203892001-0101', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000677', '2141203892017-0135', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140268', '2141203892017-0637', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140281', '2141203892017-0450', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000002', 'R90AKVHW', 'Lenovo ThinkPad L540, 14, Intel Core i5-4300M 2.6-3.3GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600014', '2141203892017-0199', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000326', 'PC00NPKJ', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 8, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140287', '2141203892017-0096', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600067', '2141203892017-0064', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600012', '2141203892017-0078', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600064', '2141203892017-0295', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000040', '11258709', 'Intel(R) Core(TM) i3-3250 CPU @ 3.50GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('000000202309200000000070', 'PB0V3EZ', 'Intel(R) Celeron(R) CPU G540 @ 2.50GHz ,4 ,250', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600000504', '10894062', 'Intel(R) Core(TM)2 Duo CPU���� E8400� @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600016', '2141203892017-0007', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600038', '2141203892017-0076', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141004', '11514940', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000029', 'MSAC71B5S0113321', 'MSI Wind TOP, 21.5, Intel Core i3-2100 @ 3.1GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140583', 'NXMPGER009513078186600', 'Acer Aspire V3-371-31C2, 13.3, Intel Core i3 4005U 1.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141007', '11514933', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140254', '2141203892001-0225', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140205', '2141203892001-0010', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34141008', '11528887', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600021', '2141203892017-0553', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140129', '2141203892017-0399', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140172', '2141203892017-0435', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140116', '2141126892014-0080', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140276', '2141203892001-0208', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000407', '381132-014', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000557', '11514953', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140998', '11514946', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140841', '11514954', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140259', '2141126892014-0037', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000631', '2141203892001-0113', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000503', '10894071', 'Intel(R) Core(TM) i3-3250 CPU @ 3.50GHz ,8 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600010', '2141105830606-0013', 'Intel(R) Core(TM) i3-3250 CPU @ 3.50GHz ,8 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140119', '2141203892017-0391', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140213', '2141203892017-0473', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430205450007', '11514944', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000661', '2141203892017-0046', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140275', '2141203892017-0072', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140219', '2141203892001-0086', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140236', '2141203892001-0071', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140115', '2141126892014-0052', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140210', '2141126892014-0081', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140113', '2141203892017-0180', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140123', '2141203892017-0110', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600069', '2141203892001-0176', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140991', '11489258', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620000000623', '2141203892017-0658', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202000012', '11489216', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140235', '2141203892001-0038', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140228', '2141203892001-0143', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140120', '2141126892014-0053', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430205450010', '11514937', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140223', '2141126892014-0003', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430205450008', '11514928', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600040', '2141203892017-0285', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430202600046', '2141203892017-0276', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140256', '2141203892017-0449', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,1000', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000404', '380872-008', 'DEPO Neos C522, 21.5, Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140580', 'NXMPGER009513078266600', 'Acer Aspire V3-371-31C2, 13.3, Intel Core i3 4005U 1.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140232', '2141203892017-0564', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('341430205450005', '11529117', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('343202620150000515', '9029784', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140249', '2141203892017-0542', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140987', '11514956', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140820', '11489133', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140582', 'NXMPGER009513077FF6600', 'Acer Aspire V3-371-31C2, 13.3, Intel Core i3 4005U 1.7GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140214', '2141203892017-0577', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140242', '2141203892017-0544', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140233', '2141203892001-0157', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,4 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140834', '11489191', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz ,8 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140289', '2141203892017-0066', 'Intel(R) Core(TM) i3-4010U CPU @ 1.70GHz ,12 ,500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('34140823', '11488958', 'Intel(R) Core(TM) i3-4150T CPU @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000327', 'PC00NNPW', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000329', 'PC00MZR3', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000334', 'PC00MWZV', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000338', 'PC00NMG6', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000339', 'PC00MY2N', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000350', 'PC00MZRB', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000373', 'PC00NM4H', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000374', 'PC00NM4D', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000378', 'PC00MXX2', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000325', 'PC00MWZW', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000328', 'PC00NMAW', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000355', 'PC00NMAX', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000356', 'PC00MWZN', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000368', 'PC00MZTV', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000375', 'PC00NM4M', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('110134202309200000000389', 'PC00NPNR', 'Intel(R) Pentium(R) CPU G3220 @ 3.00GHz, 4, 500', NULL);
INSERT INTO public.equipment (id, serial, description, sticker) VALUES ('11111111', '11111111', 'Тестовый ПК', '11111111');


--
-- Data for Name: cryptography_key_document; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_key_document (id, serial, received_from, received_at, cryptography_version_id, carrier_id, owner_id, equipment_id) VALUES (18, '0feb014a', 'Изготовлены самостоятельно', '2024-09-16', 37, 3, 9, '343202620000000598');
INSERT INTO public.cryptography_key_document (id, serial, received_from, received_at, cryptography_version_id, carrier_id, owner_id, equipment_id) VALUES (19, 'GladunovaYUV_2024_pkiClient', 'Изготовлены самостоятельно', '2024-09-17', 37, 1, 9, '343202620000000598');
INSERT INTO public.cryptography_key_document (id, serial, received_from, received_at, cryptography_version_id, carrier_id, owner_id, equipment_id) VALUES (20, 'DilyanovaKN_2024_pkiClient', 'Изготовлены самостоятельно', '2024-09-18', 33, 1, 11, '34140167');
INSERT INTO public.cryptography_key_document (id, serial, received_from, received_at, cryptography_version_id, carrier_id, owner_id, equipment_id) VALUES (16, '0feb014b', 'Изготовлены самостоятельно', '2024-09-13', 37, 3, 7, '34140128');
INSERT INTO public.cryptography_key_document (id, serial, received_from, received_at, cryptography_version_id, carrier_id, owner_id, equipment_id) VALUES (17, 'VasilievaVV_PKI_Client', 'Изготовлены самостоятельно', '2024-09-13', 37, 1, 7, '34140128');


--
-- Data for Name: cryptography_hardware_logbook; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_hardware_logbook (id, happened_at, cryptography_version_id, record_type, key_document_id, remove_action_id, removed_at, comment, created_at, updated_at, equipment_id) VALUES (3, '2024-09-13', 37, 'C_INSTALL', 16, NULL, NULL, NULL, '2024-09-13 11:28:48.79953', '2024-09-13 11:28:48.79953', '34140128');
INSERT INTO public.cryptography_hardware_logbook (id, happened_at, cryptography_version_id, record_type, key_document_id, remove_action_id, removed_at, comment, created_at, updated_at, equipment_id) VALUES (4, '2024-09-13', 37, 'KD_INSTALL', 17, NULL, NULL, NULL, '2024-09-13 11:28:49.119795', '2024-09-13 11:28:49.119795', '34140128');
INSERT INTO public.cryptography_hardware_logbook (id, happened_at, cryptography_version_id, record_type, key_document_id, remove_action_id, removed_at, comment, created_at, updated_at, equipment_id) VALUES (5, '2024-09-17', 37, 'C_INSTALL', 18, NULL, NULL, NULL, '2024-09-18 06:01:10.699177', '2024-09-18 06:01:10.699177', '343202620000000598');
INSERT INTO public.cryptography_hardware_logbook (id, happened_at, cryptography_version_id, record_type, key_document_id, remove_action_id, removed_at, comment, created_at, updated_at, equipment_id) VALUES (6, '2024-09-17', 37, 'KD_INSTALL', 19, NULL, NULL, NULL, '2024-09-18 06:01:11.600781', '2024-09-18 06:01:11.600781', '343202620000000598');
INSERT INTO public.cryptography_hardware_logbook (id, happened_at, cryptography_version_id, record_type, key_document_id, remove_action_id, removed_at, comment, created_at, updated_at, equipment_id) VALUES (7, '2024-09-18', 33, 'KD_INSTALL', 20, NULL, NULL, NULL, '2024-09-18 10:56:31.005993', '2024-09-18 10:56:31.005993', '34140167');


--
-- Data for Name: cryptography_instance_logbook; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_instance_logbook (id, happened_at, key_document_is_unexpired, comment, cryptography_version_id, key_document_id, install_action_id, remove_action_id, equipment_id, responsible_user_id, created_at, updated_at) VALUES (4, '2024-09-13', true, '', 37, 16, 21, NULL, '34140128', 7, '2024-09-13 11:28:48.660757', '2024-09-13 11:28:48.660757');
INSERT INTO public.cryptography_instance_logbook (id, happened_at, key_document_is_unexpired, comment, cryptography_version_id, key_document_id, install_action_id, remove_action_id, equipment_id, responsible_user_id, created_at, updated_at) VALUES (5, '2024-09-13', false, '', 37, 17, 21, NULL, '34140128', 7, '2024-09-13 11:28:49.036247', '2024-09-13 11:28:49.036247');
INSERT INTO public.cryptography_instance_logbook (id, happened_at, key_document_is_unexpired, comment, cryptography_version_id, key_document_id, install_action_id, remove_action_id, equipment_id, responsible_user_id, created_at, updated_at) VALUES (6, '2024-09-17', true, '', 37, 18, 22, NULL, '343202620000000598', 9, '2024-09-18 06:01:10.537131', '2024-09-18 06:01:10.537131');
INSERT INTO public.cryptography_instance_logbook (id, happened_at, key_document_is_unexpired, comment, cryptography_version_id, key_document_id, install_action_id, remove_action_id, equipment_id, responsible_user_id, created_at, updated_at) VALUES (7, '2024-09-17', false, '', 37, 19, 22, NULL, '343202620000000598', 9, '2024-09-18 06:01:11.468462', '2024-09-18 06:01:11.468462');
INSERT INTO public.cryptography_instance_logbook (id, happened_at, key_document_is_unexpired, comment, cryptography_version_id, key_document_id, install_action_id, remove_action_id, equipment_id, responsible_user_id, created_at, updated_at) VALUES (8, '2024-09-18', false, '', 33, 20, 23, NULL, '34140167', 11, '2024-09-18 10:56:30.679234', '2024-09-18 10:56:30.679234');


--
-- Data for Name: cryptography_logbook; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (2, '2023-02-20', '', 32, 8, NULL, '2024-08-28 07:40:55.973963', '2024-08-28 07:40:55.973963');
INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (4, '2023-02-16', '', 34, 10, NULL, '2024-08-28 08:17:54.089007', '2024-08-28 08:17:54.089007');
INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (5, '2024-04-04', '', 35, 11, NULL, '2024-08-28 08:27:47.428248', '2024-08-28 08:27:47.428248');
INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (6, '2024-04-04', '', 36, 12, NULL, '2024-08-28 08:32:29.595749', '2024-08-28 08:32:29.595749');
INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (7, '2024-04-22', '', 37, 13, NULL, '2024-08-28 09:10:19.586144', '2024-08-28 09:10:19.586144');
INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (8, '2024-04-22', '', 38, 14, NULL, '2024-08-28 09:27:46.486774', '2024-08-28 09:27:46.486774');
INSERT INTO public.cryptography_logbook (id, happened_at, comment, cryptography_version_id, install_action_id, remove_action_id, created_at, updated_at) VALUES (3, '2023-02-16', '', 33, 9, 16, '2024-08-28 08:11:02.344726', '2024-09-03 13:59:22.673349');


--
-- Data for Name: cryptography_personal_account; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.cryptography_personal_account (id, user_id, happened_at, cryptography_version_id, key_document_id, equipment_id, install_action_id, removed_at, remove_action_id, comment, created_at, updated_at) VALUES (2, 7, '2024-09-13', 37, 16, '34140128', 21, NULL, NULL, NULL, '2024-09-13 11:28:48.881021', '2024-09-13 11:28:48.881021');
INSERT INTO public.cryptography_personal_account (id, user_id, happened_at, cryptography_version_id, key_document_id, equipment_id, install_action_id, removed_at, remove_action_id, comment, created_at, updated_at) VALUES (3, 7, '2024-09-13', 37, 17, '34140128', 21, NULL, NULL, NULL, '2024-09-13 11:28:49.168976', '2024-09-13 11:28:49.168976');
INSERT INTO public.cryptography_personal_account (id, user_id, happened_at, cryptography_version_id, key_document_id, equipment_id, install_action_id, removed_at, remove_action_id, comment, created_at, updated_at) VALUES (4, 9, '2024-09-17', 37, 18, '343202620000000598', 22, NULL, NULL, NULL, '2024-09-18 06:01:11.107076', '2024-09-18 06:01:11.107076');
INSERT INTO public.cryptography_personal_account (id, user_id, happened_at, cryptography_version_id, key_document_id, equipment_id, install_action_id, removed_at, remove_action_id, comment, created_at, updated_at) VALUES (5, 9, '2024-09-17', 37, 19, '343202620000000598', 22, NULL, NULL, NULL, '2024-09-18 06:01:11.818136', '2024-09-18 06:01:11.818136');
INSERT INTO public.cryptography_personal_account (id, user_id, happened_at, cryptography_version_id, key_document_id, equipment_id, install_action_id, removed_at, remove_action_id, comment, created_at, updated_at) VALUES (6, 11, '2024-09-18', 33, 20, '34140167', 23, NULL, NULL, NULL, '2024-09-18 10:56:31.244691', '2024-09-18 10:56:31.244691');


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: user
--



--
-- Name: cryptography_act_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_act_records_id_seq', 90, true);


--
-- Name: cryptography_hardware_logbook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_hardware_logbook_id_seq', 37, true);


--
-- Name: cryptography_instance_logbook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_instance_logbook_id_seq', 39, true);


--
-- Name: cryptography_key_carrier_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_key_carrier_types_id_seq', 12, true);


--
-- Name: cryptography_key_carriers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_key_carriers_id_seq', 4, true);


--
-- Name: cryptography_key_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_key_documents_id_seq', 51, true);


--
-- Name: cryptography_logbook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_logbook_id_seq', 9, true);


--
-- Name: cryptography_manufacturers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_manufacturers_id_seq', 3, true);


--
-- Name: cryptography_models_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_models_id_seq', 6, true);


--
-- Name: cryptography_personal_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_personal_accounts_id_seq', 36, true);


--
-- Name: cryptography_versions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.cryptography_versions_id_seq', 39, true);


--
-- Name: employee_departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.employee_departments_id_seq', 6, true);


--
-- Name: employee_location_buildings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.employee_location_buildings_id_seq', 7, true);


--
-- Name: employee_locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.employee_locations_id_seq', 7, true);


--
-- Name: employee_organisations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.employee_organisations_id_seq', 2, true);


--
-- Name: employee_positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.employee_positions_id_seq', 11, true);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.employees_id_seq', 12, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

