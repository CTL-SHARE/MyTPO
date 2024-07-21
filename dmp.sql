--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Postgres.app)
-- Dumped by pg_dump version 16.2 (Postgres.app)

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
-- Name: xdf; Type: SCHEMA; Schema: -; Owner: Taylor
--

CREATE SCHEMA xdf;


ALTER SCHEMA xdf OWNER TO "Taylor";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: listening_conversation; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.listening_conversation (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    audio_url text,
    question_html text,
    question_clean text,
    choices text[],
    answers text[],
    access_time time without time zone,
    solution text,
    transcription text
);


ALTER TABLE xdf.listening_conversation OWNER TO "Taylor";

--
-- Name: listening_lecture; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.listening_lecture (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    audio_url text,
    question_html text,
    question_clean text,
    choices text[],
    answers text[],
    access_time time without time zone,
    solution text,
    transcription text
);


ALTER TABLE xdf.listening_lecture OWNER TO "Taylor";

--
-- Name: reading; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.reading (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    passage_html text,
    passage_clean text,
    question_html text,
    question_clean text,
    choices text[],
    answers text[],
    access_time time without time zone,
    solution text
);


ALTER TABLE xdf.reading OWNER TO "Taylor";

--
-- Name: speaking_q1; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.speaking_q1 (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    prompt_html text,
    prompt_clean text,
    example_response text,
    access_time time without time zone
);


ALTER TABLE xdf.speaking_q1 OWNER TO "Taylor";

--
-- Name: speaking_q2; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.speaking_q2 (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    passage_html text,
    passage_clean text,
    audio_url text,
    access_time time without time zone,
    transcription text,
    example_response text
);


ALTER TABLE xdf.speaking_q2 OWNER TO "Taylor";

--
-- Name: speaking_q3; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.speaking_q3 (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    passage_html text,
    passage_clean text,
    audio_url text,
    access_time time without time zone,
    transcription text,
    example_response text
);


ALTER TABLE xdf.speaking_q3 OWNER TO "Taylor";

--
-- Name: speaking_q4; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.speaking_q4 (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    audio_url text,
    access_time time without time zone,
    transcription text,
    example_response text
);


ALTER TABLE xdf.speaking_q4 OWNER TO "Taylor";

--
-- Name: writing_independent; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.writing_independent (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    passage_html text,
    passage_clean text,
    access_time time without time zone,
    example_response text
);


ALTER TABLE xdf.writing_independent OWNER TO "Taylor";

--
-- Name: writing_integrated; Type: TABLE; Schema: xdf; Owner: Taylor
--

CREATE TABLE xdf.writing_integrated (
    url text,
    examid numeric,
    uid text,
    pid text,
    timuid text,
    attributes text[],
    classexamid numeric,
    question_index integer,
    full_html text,
    caption_html text,
    caption_clean text,
    passage_html text,
    passage_clean text,
    audio_url text,
    access_time time without time zone,
    transcription text,
    example_response text
);


ALTER TABLE xdf.writing_integrated OWNER TO "Taylor";

--
-- Data for Name: listening_conversation; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.listening_conversation (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, audio_url, question_html, question_clean, choices, answers, access_time, solution, transcription) FROM stdin;
\.


--
-- Data for Name: listening_lecture; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.listening_lecture (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, audio_url, question_html, question_clean, choices, answers, access_time, solution, transcription) FROM stdin;
\.


--
-- Data for Name: reading; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.reading (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, passage_html, passage_clean, question_html, question_clean, choices, answers, access_time, solution) FROM stdin;
\.


--
-- Data for Name: speaking_q1; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.speaking_q1 (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, prompt_html, prompt_clean, example_response, access_time) FROM stdin;
\.


--
-- Data for Name: speaking_q2; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.speaking_q2 (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, passage_html, passage_clean, audio_url, access_time, transcription, example_response) FROM stdin;
\.


--
-- Data for Name: speaking_q3; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.speaking_q3 (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, passage_html, passage_clean, audio_url, access_time, transcription, example_response) FROM stdin;
\.


--
-- Data for Name: speaking_q4; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.speaking_q4 (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, audio_url, access_time, transcription, example_response) FROM stdin;
\.


--
-- Data for Name: writing_independent; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.writing_independent (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, passage_html, passage_clean, access_time, example_response) FROM stdin;
\.


--
-- Data for Name: writing_integrated; Type: TABLE DATA; Schema: xdf; Owner: Taylor
--

COPY xdf.writing_integrated (url, examid, uid, pid, timuid, attributes, classexamid, question_index, full_html, caption_html, caption_clean, passage_html, passage_clean, audio_url, access_time, transcription, example_response) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

