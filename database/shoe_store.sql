--
-- PostgreSQL database dump
--

\restrict q2d3vBz0ZFUFP9R0yEAJ6rSPmx5WELRwWSBmsYKyemgKnawiC81Wqh1N70enDpd

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-12-12 11:25:07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 226 (class 1259 OID 16472)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer NOT NULL,
    product_article character varying(20) NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16471)
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- TOC entry 5058 (class 0 OID 0)
-- Dependencies: 225
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- TOC entry 224 (class 1259 OID 16449)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer NOT NULL,
    order_date timestamp without time zone NOT NULL,
    delivery_date timestamp without time zone NOT NULL,
    pickup_point_id integer NOT NULL,
    receive_code integer NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16422)
-- Name: pickup_points; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pickup_points (
    id integer NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.pickup_points OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16421)
-- Name: pickup_points_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pickup_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pickup_points_id_seq OWNER TO postgres;

--
-- TOC entry 5059 (class 0 OID 0)
-- Dependencies: 221
-- Name: pickup_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pickup_points_id_seq OWNED BY public.pickup_points.id;


--
-- TOC entry 223 (class 1259 OID 16430)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    article character varying(20) NOT NULL,
    name character varying(100) NOT NULL,
    unit character varying(20) NOT NULL,
    price numeric(10,2) NOT NULL,
    supplier character varying(100) NOT NULL,
    manufacturer character varying(100) NOT NULL,
    category character varying(50) NOT NULL,
    discount integer NOT NULL,
    stock_quantity integer NOT NULL,
    description text,
    image_path character varying(255) DEFAULT 'picture.png'::character varying,
    CONSTRAINT products_discount_check CHECK ((discount >= 0)),
    CONSTRAINT products_price_check CHECK ((price >= (0)::numeric)),
    CONSTRAINT products_stock_quantity_check CHECK ((stock_quantity >= 0))
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16408)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    role character varying(50) NOT NULL,
    full_name character varying(100) NOT NULL,
    login character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16407)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4877 (class 2604 OID 16475)
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- TOC entry 4875 (class 2604 OID 16425)
-- Name: pickup_points id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points ALTER COLUMN id SET DEFAULT nextval('public.pickup_points_id_seq'::regclass);


--
-- TOC entry 4874 (class 2604 OID 16411)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5052 (class 0 OID 16472)
-- Dependencies: 226
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, product_article, quantity) FROM stdin;
1	1	А112Т4	2
2	1	F635R4	2
3	2	H782T5	1
4	2	G783F5	1
5	3	J384T6	10
6	3	D572U8	10
7	4	F572H7	5
8	4	D329H3	4
9	5	А112Т4	2
10	5	F635R4	2
11	6	H782T5	1
12	6	G783F5	1
13	7	J384T6	10
14	7	D572U8	10
15	8	F572H7	5
16	8	D329H3	4
17	9	B320R5	5
18	9	G432E4	1
25	10	S213E3	5
26	10	E482R4	5
\.


--
-- TOC entry 5050 (class 0 OID 16449)
-- Dependencies: 224
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, user_id, order_date, delivery_date, pickup_point_id, receive_code, status) FROM stdin;
1	4	2025-02-27 00:00:00	2025-04-20 00:00:00	1	901	Завершен
2	1	2022-09-28 00:00:00	2025-04-21 00:00:00	11	902	Завершен
3	2	2025-03-21 00:00:00	2025-04-22 00:00:00	2	903	Завершен
4	3	2025-02-20 00:00:00	2025-04-23 00:00:00	11	904	Завершен
5	4	2025-03-17 00:00:00	2025-04-24 00:00:00	2	905	Завершен
6	1	2025-03-01 00:00:00	2025-04-25 00:00:00	15	906	Завершен
7	2	2025-02-28 00:00:00	2025-04-26 00:00:00	3	907	Завершен
8	3	2025-03-31 00:00:00	2025-04-27 00:00:00	19	908	Новый
9	4	2025-04-02 00:00:00	2025-04-28 00:00:00	5	909	Новый
10	4	2025-04-03 00:00:00	2025-04-24 00:00:00	19	910	новый
\.


--
-- TOC entry 5048 (class 0 OID 16422)
-- Dependencies: 222
-- Data for Name: pickup_points; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pickup_points (id, address) FROM stdin;
1	420151, г. Лесной, ул. Вишневая, 32
2	125061, г. Лесной, ул. Подгорная, 8
3	630370, г. Лесной, ул. Шоссейная, 24
4	400562, г. Лесной, ул. Зеленая, 32
5	614510, г. Лесной, ул. Маяковского, 47
6	410542, г. Лесной, ул. Светлая, 46
7	620839, г. Лесной, ул. Цветочная, 8
8	443890, г. Лесной, ул. Коммунистическая, 1
9	603379, г. Лесной, ул. Спортивная, 46
10	603721, г. Лесной, ул. Гоголя, 41
11	410172, г. Лесной, ул. Северная, 13
12	614611, г. Лесной, ул. Молодежная, 50
13	454311, г. Лесной, ул. Новая, 19
14	660007, г. Лесной, ул. Октябрьская, 19
15	603036, г. Лесной, ул. Садовая, 4
16	394060, г. Лесной, ул. Фрунзе, 43
17	410661, г. Лесной, ул. Школьная, 50
18	625590, г. Лесной, ул. Коммунистическая, 20
19	625683, г. Лесной, ул. 8 Марта
20	450983, г. Лесной, ул. Комсомольская, 26
21	394782, г. Лесной, ул. Чехова, 3
22	603002, г. Лесной, ул. Дзержинского, 28
23	450558, г. Лесной, ул. Набережная, 30
24	344288, г. Лесной, ул. Чехова, 1
25	614164, г. Лесной, ул. Степная, 30
26	394242, г. Лесной, ул. Коммунистическая, 43
27	660540, г. Лесной, ул. Солнечная, 25
28	125837, г. Лесной, ул. Шоссейная, 40
29	125703, г. Лесной, ул. Партизанская, 49
30	625283, г. Лесной, ул. Победы, 46
31	614753, г. Лесной, ул. Полевая, 35
32	426030, г. Лесной, ул. Маяковского, 44
33	450375, г. Лесной ул. Клубная, 44
34	625560, г. Лесной, ул. Некрасова, 12
35	630201, г. Лесной, ул. Комсомольская, 17
36	190949, г. Лесной, ул. Мичурина, 26
\.


--
-- TOC entry 5049 (class 0 OID 16430)
-- Dependencies: 223
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (article, name, unit, price, supplier, manufacturer, category, discount, stock_quantity, description, image_path) FROM stdin;
А112Т4	Ботинки	шт.	4990.00	Kari	Kari	Женская обувь	3	6	Женские Ботинки демисезонные kari	1.jpg
F635R4	Ботинки	шт.	3244.00	Обувь для вас	Marco Tozzi	Женская обувь	2	13	Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый	2.jpg
H782T5	Туфли	шт.	4499.00	Kari	Kari	Мужская обувь	4	5	Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный	3.jpg
G783F5	Ботинки	шт.	5900.00	Kari	Рос	Мужская обувь	2	8	Мужские ботинки Рос-Обувь кожаные с натуральным мехом	4.jpg
J384T6	Ботинки	шт.	3800.00	Обувь для вас	Rieker	Мужская обувь	2	16	B3430/14 Полуботинки мужские Rieker	5.jpg
D572U8	Кроссовки	шт.	4100.00	Обувь для вас	Рос	Мужская обувь	3	6	129615-4 Кроссовки мужские	6.jpg
F572H7	Туфли	шт.	2700.00	Kari	Marco Tozzi	Женская обувь	2	14	Туфли Marco Tozzi женские летние, размер 39, цвет черный	7.jpg
D329H3	Полуботинки	шт.	1890.00	Обувь для вас	Alessio Nesca	Женская обувь	4	4	Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый	8.jpg
B320R5	Туфли	шт.	4300.00	Kari	Rieker	Женская обувь	2	6	Туфли Rieker женские демисезонные, размер 41, цвет коричневый	9.jpg
G432E4	Туфли	шт.	2800.00	Kari	Kari	Женская обувь	3	15	Туфли kari женские TR-YR-413017, размер 37, цвет: черный	10.jpg
S213E3	Полуботинки	шт.	2156.00	Обувь для вас	CROSBY	Мужская обувь	3	6	407700/01-01 Полуботинки мужские CROSBY	picture.png
E482R4	Полуботинки	шт.	1800.00	Kari	Kari	Женская обувь	2	14	Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный	picture.png
S634B5	Кеды	шт.	5500.00	Обувь для вас	CROSBY	Мужская обувь	3	0	Кеды Caprice мужские демисезонные, размер 42, цвет черный	picture.png
K345R4	Полуботинки	шт.	2100.00	Обувь для вас	CROSBY	Мужская обувь	2	3	407700/01-02 Полуботинки мужские CROSBY	picture.png
O754F4	Туфли	шт.	5400.00	Обувь для вас	Rieker	Женская обувь	4	18	Туфли женские демисезонные Rieker артикул 55073-68/37	picture.png
G531F4	Ботинки	шт.	6600.00	Kari	Kari	Женская обувь	12	9	Ботинки женские зимние ROMER арт. 893167-01 Черный	picture.png
J542F5	Тапочки	шт.	500.00	Kari	Kari	Мужская обувь	13	0	Тапочки мужские Арт.70701-55-67син р.41	picture.png
B431R5	Ботинки	шт.	2700.00	Обувь для вас	Rieker	Мужская обувь	2	5	Мужские кожаные ботинки/мужские ботинки	picture.png
P764G4	Туфли	шт.	6800.00	Kari	CROSBY	Женская обувь	15	15	Туфли женские, ARGO, размер 38	picture.png
C436G5	Ботинки	шт.	10200.00	Kari	Alessio Nesca	Женская обувь	15	9	Ботинки женские, ARGO, размер 40	picture.png
F427R5	Ботинки	шт.	11800.00	Обувь для вас	Rieker	Женская обувь	15	11	Ботинки на молнии с декоративной пряжкой FRAU	picture.png
N457T5	Полуботинки	шт.	4600.00	Kari	CROSBY	Женская обувь	3	13	Полуботинки Ботинки черные зимние, мех	picture.png
D364R4	Туфли	шт.	12400.00	Kari	Kari	Женская обувь	16	5	Туфли Luiza Belly женские Kate-lazo черные из натуральной замши	picture.png
S326R5	Тапочки	шт.	9900.00	Обувь для вас	CROSBY	Мужская обувь	17	15	Мужские кожаные тапочки "Профиль С.Дали"	picture.png
L754R4	Полуботинки	шт.	1700.00	Kari	Kari	Женская обувь	2	7	Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный	picture.png
M542T5	Кроссовки	шт.	2800.00	Обувь для вас	Rieker	Мужская обувь	18	3	Кроссовки мужские TOFA	picture.png
D268G5	Туфли	шт.	4399.00	Обувь для вас	Rieker	Женская обувь	3	12	Туфли Rieker женские демисезонные, размер 36, цвет коричневый	picture.png
T324F5	Сапоги	шт.	4699.00	Kari	CROSBY	Женская обувь	2	5	Сапоги замша Цвет: синий	picture.png
K358H6	Тапочки	шт.	599.00	Kari	Rieker	Мужская обувь	20	2	Тапочки мужские син р.41	picture.png
H535R5	Ботинки	шт.	2300.00	Обувь для вас	Rieker	Женская обувь	2	7	Женские Ботинки демисезонные	picture.png
H245Y	Cool Shoes	шт.	3501.00	Stockx	Nike	Кроссовки	12	6		H245Y.png
\.


--
-- TOC entry 5046 (class 0 OID 16408)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, role, full_name, login, password) FROM stdin;
1	Администратор	Никифорова Весения Николаевна	94d5ous@gmail.com	uzWC67
2	Администратор	Сазонов Руслан Германович	uth4iz@mail.com	2L6KZG
3	Администратор	Одинцов Серафим Артёмович	yzls62@outlook.com	JlFRCZ
4	Менеджер	Степанов Михаил Артёмович	1diph5e@tutanota.com	8ntwUp
5	Менеджер	Ворсин Петр Евгеньевич	tjde7c@yahoo.com	YOyhfR
6	Менеджер	Старикова Елена Павловна	wpmrc3do@tutanota.com	RSbvHv
7	Авторизированный клиент	Михайлюк Анна Вячеславовна	5d4zbu@tutanota.com	rwVDh9
8	Авторизированный клиент	Ситдикова Елена Анатольевна	ptec8ym@yahoo.com	LdNyos
9	Авторизированный клиент	Ворсин Петр Евгеньевич	1qz4kw@mail.com	gynQMT
10	Авторизированный клиент	Старикова Елена Павловна	4np6se@mail.com	AtnDjr
\.


--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 225
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 26, true);


--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 221
-- Name: pickup_points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pickup_points_id_seq', 36, true);


--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- TOC entry 4893 (class 2606 OID 16482)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- TOC entry 4891 (class 2606 OID 16460)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 4887 (class 2606 OID 16429)
-- Name: pickup_points pickup_points_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points
    ADD CONSTRAINT pickup_points_pkey PRIMARY KEY (id);


--
-- TOC entry 4889 (class 2606 OID 16448)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (article);


--
-- TOC entry 4883 (class 2606 OID 16420)
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- TOC entry 4885 (class 2606 OID 16418)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4896 (class 2606 OID 16483)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 4897 (class 2606 OID 16488)
-- Name: order_items order_items_product_article_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_article_fkey FOREIGN KEY (product_article) REFERENCES public.products(article);


--
-- TOC entry 4894 (class 2606 OID 16466)
-- Name: orders orders_pickup_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pickup_point_id_fkey FOREIGN KEY (pickup_point_id) REFERENCES public.pickup_points(id);


--
-- TOC entry 4895 (class 2606 OID 16461)
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2025-12-12 11:25:07

--
-- PostgreSQL database dump complete
--

\unrestrict q2d3vBz0ZFUFP9R0yEAJ6rSPmx5WELRwWSBmsYKyemgKnawiC81Wqh1N70enDpd

