# KP71_Kovtun_Artem_DB1
## Лабораторна робота № 1.

### КП-71 Ковтун Артем Сергійович

Варіант 4 - "Маркетплейс"

[**Звіт**](https://github.com/demchenkov/KP72_Demchenko_Vlad_DB1/blob/master/proto%D1%81ol_lr1.doc)

**Сутності:**
1. Customers 
```
CREATE TABLE public.customers
(
    id integer NOT NULL DEFAULT nextval('customers_id_seq'::regclass),
    first_name text COLLATE pg_catalog."default" NOT NULL,
    last_name text COLLATE pg_catalog."default" NOT NULL,
    birth_date date,
    deliver_adress text COLLATE pg_catalog."default",
    CONSTRAINT customers_pkey PRIMARY KEY (id)
)
```
2. Orders:
```
CREATE TABLE public.orders
(
    id integer NOT NULL DEFAULT nextval('orders_id_seq'::regclass),
    date date NOT NULL,
    product integer NOT NULL,
    cutomer integer NOT NULL,
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT orders_cutomer_fkey FOREIGN KEY (cutomer)
        REFERENCES public.customers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT orders_product_fkey FOREIGN KEY (product)
        REFERENCES public.products (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)


```
3. Products:
```
CREATE TABLE public.products
(
    id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    price real NOT NULL,
    description text COLLATE pg_catalog."default",
    quantity integer NOT NULL,
    shop integer NOT NULL,
    photo_url text COLLATE pg_catalog."default",
    CONSTRAINT products_pkey PRIMARY KEY (id),
    CONSTRAINT products_shop_fkey FOREIGN KEY (shop)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
```
4. Shops: 
```
CREATE TABLE public.shops
(
    image_url text COLLATE pg_catalog."default",
    website_url text COLLATE pg_catalog."default",
    shop_name text COLLATE pg_catalog."default",
    id integer NOT NULL DEFAULT nextval('shops_id_seq'::regclass),
    CONSTRAINT shops_pkey PRIMARY KEY (id)
)
```
