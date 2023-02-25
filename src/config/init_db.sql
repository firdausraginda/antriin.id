-- Type: queue_user_status
-- DROP TYPE IF EXISTS public.queue_user_status;
CREATE TYPE public.queue_user_status AS ENUM ('in_queue', 'done');

ALTER TYPE public.queue_user_status OWNER TO super_admin;

-- Type: queue_status
-- DROP TYPE IF EXISTS public.queue_status;
CREATE TYPE public.queue_status AS ENUM ('active', 'hold', 'off');

ALTER TYPE public.queue_status OWNER to super_admin;

-- Table: public.admin
-- DROP TABLE IF EXISTS public.admin;
CREATE TABLE IF NOT EXISTS public.admin (
    id SERIAL NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT admin_pkey_id PRIMARY KEY (id),
    CONSTRAINT admin_unique_email UNIQUE (email) INCLUDE(email)
) TABLESPACE pg_default;

ALTER TABLE
    IF EXISTS public.admin OWNER to super_admin;

-- Table: public.organization
-- DROP TABLE IF EXISTS public.organization;
CREATE TABLE IF NOT EXISTS public.organization (
    id SERIAL NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default",
    admin_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT organization_pkey_id PRIMARY KEY (id),
    CONSTRAINT organization_unique_admin_id UNIQUE (admin_id) INCLUDE(admin_id),
    CONSTRAINT organization_fkey_admin_id FOREIGN KEY (admin_id) REFERENCES public.admin (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE NOT VALID
) TABLESPACE pg_default;

ALTER TABLE
    IF EXISTS public.organization OWNER to super_admin;

-- Table: public.queue
-- DROP TABLE IF EXISTS public.queue;
CREATE TABLE IF NOT EXISTS public.queue (
    id SERIAL NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default",
    short_url character varying(5) COLLATE pg_catalog."default" NOT NULL,
    current_queue_number integer NOT NULL DEFAULT 0,
    total_queue_number integer NOT NULL DEFAULT 0,
    admin_id integer NOT NULL,
    status queue_status NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT queue_pkey_id PRIMARY KEY (id),
    CONSTRAINT name UNIQUE (name) INCLUDE(name),
    CONSTRAINT queue_fkey_admin_id FOREIGN KEY (admin_id) REFERENCES public.admin (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID
) TABLESPACE pg_default;

ALTER TABLE
    IF EXISTS public.queue OWNER to super_admin;

-- Table: public.user
-- DROP TABLE IF EXISTS public."user";
CREATE TABLE IF NOT EXISTS public."user" (
    id SERIAL NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT user_pkey_id PRIMARY KEY (id),
    CONSTRAINT email UNIQUE (email) INCLUDE(email)
) TABLESPACE pg_default;

ALTER TABLE
    IF EXISTS public."user" OWNER to super_admin;

-- Table: public.queue_user
-- DROP TABLE IF EXISTS public.queue_user;
CREATE TABLE IF NOT EXISTS public.queue_user (
    id SERIAL NOT NULL,
    queue_number integer NOT NULL,
    queue_id integer NOT NULL,
    user_id integer NOT NULL,
    status queue_user_status NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT queue_user_pkey PRIMARY KEY (id),
    CONSTRAINT queue_user_fkey_queue_id FOREIGN KEY (queue_id) REFERENCES public.queue (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID,
    CONSTRAINT queue_user_fkey_user_id FOREIGN KEY (user_id) REFERENCES public."user" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID
) TABLESPACE pg_default;

ALTER TABLE
    IF EXISTS public.queue_user OWNER to super_admin;