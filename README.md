# KP71_Kovtun_Artem_DB1
## Лабораторна робота № 1.

### КП-71 Ковтун Артем Сергійович

Варіант 4 - "Маркетплейс"

[**Звіт**](https://github.com/demchenkov/KP72_Demchenko_Vlad_DB1/blob/master/proto%D1%81ol_lr1.doc)

**Сутності:**
1. Customers 
```
CREATE TABLE public.customer
(
    id bigint NOT NULL,
    first_name text COLLATE pg_catalog."default",
    last_name text COLLATE pg_catalog."default",
    birth_date date,
    deliver_adress text COLLATE pg_catalog."default",
    CONSTRAINT customer_pkey PRIMARY KEY (id)
)
```
2. Orders:
```
CREATE TABLE public.orders
(
    id bigint NOT NULL,
    product bigint,
    date date,
    customer bigint,
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT customer_fk FOREIGN KEY (customer)
        REFERENCES public.customer (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT product_fk FOREIGN KEY (product)
        REFERENCES public.products (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

```
3. Products:
```
CREATE TABLE public.products
(
    id bigint NOT NULL,
    name text COLLATE pg_catalog."default",
    price real,
    description text COLLATE pg_catalog."default",
    quantity bigint,
    shop bigint,
    CONSTRAINT products_pkey PRIMARY KEY (id),
    CONSTRAINT shop_fk FOREIGN KEY (shop)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)
```
4. Shops: 
```
CREATE TABLE public.shops
(
    id bigint NOT NULL,
    adress text COLLATE pg_catalog."default",
    image_url text COLLATE pg_catalog."default",
    shop_name text COLLATE pg_catalog."default",
    CONSTRAINT shops_pkey PRIMARY KEY (id)
)
```
