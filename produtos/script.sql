-- public.produtos definition

-- Drop table

-- DROP TABLE public.produtos;

CREATE TABLE public.produtos (
	id int4 primary key,
	produto_master varchar(255) null,
	produto varchar(255) NULL,
	ano varchar(4) NULL,
	valor numeric NULL
);