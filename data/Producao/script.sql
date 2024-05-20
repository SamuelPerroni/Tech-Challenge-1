-- public.produtos definition

-- Drop table

-- DROP TABLE public.produtos;

-- public.products definition

-- Drop table

-- DROP TABLE public.products;

CREATE TABLE public.products (
	id int4 NOT NULL,
	product_type varchar(255) NULL,
	product varchar(255) NULL,
	"year" varchar(4) NULL,
	production numeric NULL,
	CONSTRAINT produtos_pkey PRIMARY KEY (id)
);