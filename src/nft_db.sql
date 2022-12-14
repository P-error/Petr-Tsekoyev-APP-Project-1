DROP TABLE IF EXISTS public.nfts;
DROP TABLE IF EXISTS public.testvalues;
DROP TABLE IF EXISTS public.users;


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

CREATE TABLE public.users (
	username character varying,
	fullname character varying,
	_hashed_password character varying,		
	password character varying
);

CREATE TABLE public.nfts (
    nft_address character varying,
    nft_metadata character varying
);
ALTER TABLE public.nfts OWNER TO postgres;


CREATE TABLE public.testvalues (
    randomstring character varying(50)
);
ALTER TABLE public.testvalues OWNER TO postgres;




