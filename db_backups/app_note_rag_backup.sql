--
-- PostgreSQL database dump
--

\restrict HXDV3b06ujQbEWDKZyH8Vc7dgdWrpcgrLsdA4ybxo8TE9Ej4kPWA94kXAzCvBB9

-- Dumped from database version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: notes; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public.notes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title text,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.notes OWNER TO app_user;

--
-- Name: notes_id_seq; Type: SEQUENCE; Schema: public; Owner: app_user
--

ALTER TABLE public.notes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.notes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: summaries; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public.summaries (
    id integer NOT NULL,
    note_id integer NOT NULL,
    summary_text text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.summaries OWNER TO app_user;

--
-- Name: summaries_id_seq; Type: SEQUENCE; Schema: public; Owner: app_user
--

ALTER TABLE public.summaries ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.summaries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO app_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: app_user
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: notes; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public.notes (id, user_id, title, content, created_at, updated_at) FROM stdin;
2	4	AI Research	This note contains information about LangGraph architecture.	2026-09-30 07:17:52.535759	2026-09-30 07:17:52.535759
3	5	Persistence Test	This data must survive a Colab runtime reset.	2026-09-30 11:02:48.384922	2026-09-30 11:02:48.384922
5	1	Agent Test	Hello. This note was created by LangGraph.	2026-09-30 11:13:47.557927	2026-09-30 11:13:47.557927
\.


--
-- Data for Name: summaries; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public.summaries (id, note_id, summary_text, created_at) FROM stdin;
1	2	A note about LangGraph architecture and AI workflows.	2026-09-30 07:17:52.562457
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public.users (id, username, created_at) FROM stdin;
1	Ali	2026-09-30 07:13:46.406642
3	Note_test	2026-09-30 07:15:57.83887
4	Summary_test	2026-09-30 07:17:52.511543
5	persistence_test	2026-09-30 11:02:48.359273
\.


--
-- Name: notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_user
--

SELECT pg_catalog.setval('public.notes_id_seq', 5, true);


--
-- Name: summaries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_user
--

SELECT pg_catalog.setval('public.summaries_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_user
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (id);


--
-- Name: summaries summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.summaries
    ADD CONSTRAINT summaries_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: notes notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: summaries summaries_note_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.summaries
    ADD CONSTRAINT summaries_note_id_fkey FOREIGN KEY (note_id) REFERENCES public.notes(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict HXDV3b06ujQbEWDKZyH8Vc7dgdWrpcgrLsdA4ybxo8TE9Ej4kPWA94kXAzCvBB9

