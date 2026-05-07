--
-- PostgreSQL database dump
--

\restrict 8ylh9uFzeHzM35uu669856CC5cpgHFmQMQR4AvkLagrbQJBdi9yRCQsIgkzDa9V

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: manu
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO manu;

--
-- Name: todos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.todos (
    id integer NOT NULL,
    titulo character varying(200) DEFAULT NULL::character varying,
    descripcion character varying(200) DEFAULT NULL::character varying,
    prioridad integer,
    completada boolean,
    "dueño_id" integer
);


ALTER TABLE public.todos OWNER TO manu;

--
-- Name: todos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.todos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.todos_id_seq OWNER TO manu;

--
-- Name: todos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.todos_id_seq OWNED BY public.todos.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    email character varying(200) DEFAULT NULL::character varying,
    nombre_usu character varying(45) DEFAULT NULL::character varying,
    nombre character varying(45) DEFAULT NULL::character varying,
    apellido character varying(45) DEFAULT NULL::character varying,
    hash_password character varying(200) DEFAULT NULL::character varying,
    activo boolean,
    rol character varying(45) DEFAULT NULL::character varying,
    tel character varying
);


ALTER TABLE public.usuarios OWNER TO manu;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO manu;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: todos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.todos ALTER COLUMN id SET DEFAULT nextval('public.todos_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: manu
--

COPY public.alembic_version (version_num) FROM stdin;
4dbe596752be
\.


--
-- Data for Name: todos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.todos (id, titulo, descripcion, prioridad, completada, "dueño_id") FROM stdin;
1	tarea de ejemplo	probar que funciona	4	t	1
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, email, nombre_usu, nombre, apellido, hash_password, activo, rol, tel) FROM stdin;
2	ejemplo@gmail.com	ejemplo	Ejemplo	Real	$2b$12$5d77wxNY54YTWZDJxRgyvuqeqbf2ZEr3cYjhB5I0Z1VzzTAS/e/la	t	admin	123456789
1	yo@gmail.com	yo	Manuel	Álvarez	$2b$12$yoY.yh3oUAK.4QR4LBfuz.iHnYpIG0MZpS9pBGN6n48bZkzOaZnWG	t	admin	587632154
\.


--
-- Name: todos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.todos_id_seq', 1, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: manu
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: todos todos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.todos
    ADD CONSTRAINT todos_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: todos todos_dueño_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.todos
    ADD CONSTRAINT "todos_dueño_id_fkey" FOREIGN KEY ("dueño_id") REFERENCES public.usuarios(id);


--
-- Name: TABLE todos; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.todos TO manu;


--
-- Name: TABLE usuarios; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.usuarios TO manu;


--
-- PostgreSQL database dump complete
--

\unrestrict 8ylh9uFzeHzM35uu669856CC5cpgHFmQMQR4AvkLagrbQJBdi9yRCQsIgkzDa9V

