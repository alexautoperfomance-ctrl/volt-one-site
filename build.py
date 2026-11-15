#!/usr/bin/env python3
"""Генератор статического сайта VOLT ONE.
Фото моделей: положите файлы в img/models/<slug>/ (jpg/webp), имена сортируются по алфавиту,
первое фото становится обложкой карточки. Затем запустите: python3 build.py"""
import os, json, glob, html
ROOT=os.path.dirname(os.path.abspath(__file__))
PHONE='+7-913-943-88-14'; TEL='tel:+79139438814'; WA='https://wa.me/79139438814'; TG='https://t.me/volte0ne'
ADDR='г. Новосибирск, ул. Пролетарская, 50'
SITE_URL='https://alexautoperfomance-ctrl.github.io/volt-one-site/'
POINTS=[{"name":"Пролетарская, 50","addr":ADDR,"lat":55.0248099,"lon":82.9562136,
  "route":"https://2gis.ru/novosibirsk/directions/points/%7C82.956214%2C55.02481",
  "open":"https://2gis.ru/novosibirsk/geo/82.956214%2C55.02481"}]

I={ # inline svg icons (stroke)
'bolt':'<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
'shield':'<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z"/><path d="m9 12 2 2 4-4"/>',
'spark':'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/>',
'check':'<path d="M20 6 9 17l-5-5"/>',
'box':'<path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
'wrench':'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4 2.5-2.5z"/>',
'swap':'<path d="M7 7h13l-4-4M17 17H4l4 4"/>',
'truck':'<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
'bag':'<path d="M5 8h14l-1 13H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
'key':'<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
'chat':'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
'send':'<path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z"/>',
'pin':'<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
'route':'<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h8.5a3.5 3.5 0 0 0 0-7h-9a3.5 3.5 0 0 1 0-7H16"/>',
'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
'left':'<path d="m15 18-6-6 6-6"/>','right':'<path d="m9 18 6-6-6-6"/>',
'x':'<path d="M18 6 6 18M6 6l12 12"/>',
'battery':'<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 10v4M10 10v4"/>',
'motor':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/>',
'speed':'<path d="M12 14l4-4"/><path d="M3.3 17a9 9 0 1 1 17.4 0"/>',
'road':'<path d="M8 3 4 21M16 3l4 18M12 5v2M12 11v2M12 17v2"/>',
'wheel':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
'size':'<path d="M3 21 21 3M14 3h7v7M10 21H3v-7"/>',
'seat':'<path d="M4 14c0-2 1.5-3 4-3h8c2.5 0 4 1 4 3v1H4v-1z"/><path d="M7 15v5M17 15v5M8 11V8a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v3"/>',
'rack':'<path d="M3 10h18M5 10v8M19 10v8M3 18h18M9 10v8M15 10v8"/>',
'mobile':'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
'plug':'<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0V8zM12 18v4"/>',
'alarm':'<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
'courier':'<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M6 17l4-8h5l3 8M10 9 8 5H6M15 9h3"/>',
'grid':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
'new':'<path d="M12 2l2.4 4.8 5.3.8-3.8 3.7.9 5.3L12 14.1 7.2 16.6l.9-5.3L4.3 7.6l5.3-.8z"/>',
}
WA_SVG='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.4 4.8 5-1.3A9.8 9.8 0 1 0 12 2.2zm0 17.9a8.1 8.1 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.1 8.1 0 1 1 12 20.1zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
TG_SVG='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.4 3.6 2.9 10.7c-1.3.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.6c.2.6.4.8.8.8s.6-.2.9-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.1-14.7c.3-1.3-.5-1.9-1.4-1.3zM9.6 13.9l8.6-5.4c.4-.3.8-.1.5.2l-7.4 6.7-.3 3.1-1.4-4.6z"/></svg>'
def ic(n,cls=''):
    if n=='wa': return WA_SVG
    if n=='tg': return TG_SVG
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

BIKE_SVG='''<svg viewBox="0 0 320 190" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="70" cy="138" r="40"/><circle cx="70" cy="138" r="14"/><circle cx="252" cy="138" r="40"/><circle cx="252" cy="138" r="14"/><path d="M70 138 112 70h78l20 32"/><path d="M118 70h-22l-10-16M190 70l62 68M210 102h-60l-38 36"/><path d="M228 46l-18 56M218 44h24"/><path d="M128 62h46" stroke-width="10" opacity=".55"/><rect x="138" y="94" width="64" height="20" rx="6" opacity=".55"/></svg>'''

def fmt(n): return f'{n:,}'.replace(',', '\u00a0')+'\u00a0₽'

MODELS=[
 dict(slug='u2',name='WENBOX U2 / U2 PRO',short='U2 / U2 PRO',sub='Быстрый и надёжный — для ежедневной работы курьером.',
   specs=[('battery','АКБ','50V / 45Ah','LiFePO4 (железо-фосфат)'),('motor','Мотор-колесо','1500 W',''),('speed','Скорость','до 70 км/ч','')],
   desc=['Все электровелосипеды новые, полностью подготовлены к работе и подходят для ежедневной работы курьером.'],
   rent=[('Неделя',5000),('Месяц',20000)],buy=[(8000,16),(6500,40)]),
 dict(slug='u2-big',name='WENBOX U2 BIG',short='U2 BIG',sub='Больше, мощнее, динамичнее.',
   specs=[('battery','АКБ','60V / 55Ah','LiFePO4 (железо-фосфат)'),('motor','Мотор-колесо','2500 W',''),('wheel','Колесо','130/70-12','')],
   desc=['По размеру больше, чем U2 и U2 Pro. Очень динамичный, отлично разгоняется.','Более крупные колёса и мощный мотор обеспечивают уверенную и динамичную езду.'],
   rent=[('Неделя',7000)],buy=[(9000,16)]),
 dict(slug='u5',name='WENBOX U5',short='U5',sub='Запас хода 100–120 км.',
   specs=[('battery','АКБ','60V / 45Ah','LiFePO4 (железо-фосфат)'),('motor','Мотор-колесо','1500 W',''),('road','Запас хода','100–120 км','')],
   desc=['Все электровелосипеды новые, полностью подготовлены к работе и подходят для ежедневной работы курьером.'],
   rent=[('Неделя',4500),('Месяц',17000)],buy=[]),
 dict(slug='r9',name='WENBOX R9',short='R9',sub='Компактнее и манёвреннее — для работы в городе.',
   specs=[('battery','АКБ','60V / 45Ah','LiFePO4 (железо-фосфат)'),('motor','Мотор-колесо','1500 W',''),('size','Размер','Немного меньше U2','')],
   desc=['Немного меньше U2 — компактнее и манёвреннее, особенно удобно для работы в городе.'],
   rent=[('Неделя',4000)],buy=[(6500,16),(5000,40)]),
]

def photos(slug):
    fs=sorted(glob.glob(os.path.join(ROOT,'img/models',slug,'*.webp')))
    return ['img/models/%s/%s'%(slug,os.path.basename(f)) for f in fs]

def head(title,desc,p,canon,og_img='img/og.jpg'):
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#141210"><link rel="canonical" href="{SITE_URL}{canon}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="VOLT ONE">
<meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE_URL}{canon}"><meta property="og:image" content="{SITE_URL}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}img/brand/favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}img/brand/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{p}img/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Unbounded:wght@400;500;600;700&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/style.css?v=6">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":"VOLT ONE","description":"Аренда, аренда с выкупом и продажа электровелосипедов для курьеров","telephone":"+79139438814","address":{"@type":"PostalAddress","streetAddress":"ул. Пролетарская, 50","addressLocality":"Новосибирск","addressCountry":"RU"},"geo":{"@type":"GeoCoordinates","latitude":POINTS[0]['lat'],"longitude":POINTS[0]['lon']}},ensure_ascii=False)}</script>
</head><body><div class="noise"></div>'''

def header(p,active,solid=False):
    home=p or './'
    links=[('Модели',f'{p}catalog/','catalog'),('Преимущества',f'{home}#adv','adv'),('Комплектация',f'{home}#kit','kit'),('Сервис',f'{home}#service','service'),('Контакты',f'{home}#contacts','contacts')]
    nav=''.join(f'<a href="{u}"{" class=active" if k==active else ""}>{t}</a>' for t,u,k in links)
    mm=''.join(f'<a class="mm-link" href="{u}">{t}{ic("arrow")}</a>' for t,u,k in links)
    return f'''<header class="header{' solid' if solid else ''}"><div class="container header-in">
<a class="logo" href="{home}" aria-label="VOLT ONE — на главную"><img src="{p}img/brand/mark.svg" alt="VOLT ONE" width="78" height="34"><span class="logo-txt"><b>VOLT ONE</b><small>Аренда · Продажа · Запчасти</small></span></a>
<nav class="nav">{nav}</nav>
<div class="header-cta"><a class="header-phone" href="{TEL}">{PHONE}</a><a class="btn btn-gold btn-sm" href="{WA}" target="_blank" rel="noopener">{ic('wa')}Написать в WhatsApp</a><a class="icon-btn" href="{TG}" target="_blank" rel="noopener" aria-label="Написать в Telegram" title="Telegram @volte0ne">{ic('tg')}</a></div>
<button class="burger" aria-label="Меню" aria-expanded="false"><span></span></button></div></header>
<div class="mobile-menu">{mm}<div class="mm-contacts"><a class="btn btn-gold btn-block" href="{TEL}">{ic('phone')}{PHONE}</a><a class="btn btn-ghost btn-block" href="{WA}" target="_blank" rel="noopener">{ic('wa')}Написать в WhatsApp</a><a class="btn btn-ghost btn-block" href="{TG}" target="_blank" rel="noopener">{ic('tg')}Написать в Telegram</a><p class="addr">{ADDR}</p></div></div>'''

def footer(p):
    home=p or './'
    ml=''.join(f'<li><a href="{p}catalog/{m["slug"]}/">{m["name"]}</a></li>' for m in MODELS)
    return f'''<footer class="footer"><div class="container"><div class="foot-grid">
<div class="foot-about"><a class="logo" href="{home}"><img src="{p}img/brand/mark.svg" alt="VOLT ONE" width="78" height="34"><span class="logo-txt"><b>VOLT ONE</b><small>Аренда · Продажа · Запчасти</small></span></a><p>Новые электровелосипеды WENBOX для курьеров. Аренда, аренда с выкупом, без залога. Собственный сервис.</p></div>
<div><h4>Модели</h4><ul>{ml}</ul></div>
<div><h4>Разделы</h4><ul><li><a href="{p}catalog/">Каталог</a></li><li><a href="{home}#adv">Преимущества</a></li><li><a href="{home}#service">Сервис</a></li><li><a href="{home}#steps">Как начать</a></li><li><a href="{home}#contacts">Контакты</a></li></ul></div>
<div><h4>Контакты</h4><ul><li><a href="{TEL}">{PHONE}</a></li><li><a class="foot-ic" href="{WA}" target="_blank" rel="noopener">{ic('wa')}Написать в WhatsApp</a></li><li><a class="foot-ic" href="{TG}" target="_blank" rel="noopener">{ic('tg')}Написать в Telegram · @volte0ne</a></li><li style="color:var(--muted)">{ADDR}</li></ul></div>
</div><div class="foot-bottom"><span>© 2026 VOLT ONE. Аренда · Продажа · Запчасти</span><span>Новая техника · Без залога · Собственный сервис · Аренда с выкупом</span></div></div></footer>
<div class="mbar"><a class="btn btn-gold" href="{TEL}">{ic('phone')}Позвонить</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ic('wa')}WhatsApp</a></div>
<script src="{p}assets/main.js?v=6" defer></script></body></html>'''

def media(m,p,cls=''):
    ph=photos(m['slug'])
    if ph:
        w=p+ph[0]; j=w[:-5]+'.jpg'
        return f'<picture><source srcset="{w}" type="image/webp"><img src="{j}" alt="{m["name"]} — фото" loading="lazy" decoding="async"></picture>'
    return f'<div class="ph">{BIKE_SVG}<small>Фото скоро</small></div>'

def price_block(m,full=False):
    rent=''.join(f'<div class="price-row"><span>{k}</span><b>{fmt(v)}</b></div>' for k,v in m['rent'])
    if m['buy']:
        buy=''.join(f'<div class="price-row"><span>{w} недель</span><b>{fmt(v)}<small>/нед</small></b></div>' for v,w in m['buy'])
    else:
        buy='<p class="price-none">Для этой модели — обычная аренда. Про выкуп уточняйте по телефону.</p>'
    return rent,buy

def card(m,p,i):
    rent,buy=price_block(m)
    badges='<span class="badge solid">Без залога</span>'+('<span class="badge">Выкуп</span>' if m['buy'] else '')
    sp=''.join(f'<div><b>{v}</b><span>{k}</span></div>' for _,k,v,_ in m['specs'])
    return f'''<article class="mcard rv d{i%4}"><div class="mcard-media"><div class="mcard-badges">{badges}</div>{media(m,p)}</div>
<div class="mcard-body"><h3>{m['name']}</h3><p class="sub">{m['sub']}</p><div class="specs-mini">{sp}</div>
<div class="price-box"><div class="p-rent">{rent}</div><div class="p-buy">{buy}</div></div>
<a class="more stretched" href="{p}catalog/{m['slug']}/">Подробнее<i>{ic('arrow')}</i></a></div></article>'''

def seg(target):
    return f'<div class="seg" role="tablist" data-target="{target}"><span class="pill"></span><button class="on" data-mode="rent" role="tab">Аренда</button><button data-mode="buy" role="tab">Выкуп</button></div>'

ADV=[('shield','Без залога','Берёте электровелосипед без залога.'),
('new','Только новая техника','Все электровелосипеды новые.'),
('check','Полностью готовы к работе','Подготовлены для ежедневной работы курьером.'),
('box','Комплектация на выбор','Кофр, двойная сидушка, багажник.'),
('plug','Всё нужное — в стоимости','Держатель для телефона, зарядное устройство и сигнализация.'),
('wrench','Собственный сервис','Быстрое обслуживание и ремонт.'),
('swap','Подменный — бесплатно','Если ремонт занимает больше времени, даём подменный электровелосипед.'),
('key','Аренда с выкупом','Возможна аренда с последующим выкупом.')]

def contacts_block():
    pts=json.dumps(POINTS,ensure_ascii=False)
    return f'''<section class="section" id="contacts"><div class="container">
<div class="section-head rv"><span class="eyebrow">Где находимся</span><h2>Приезжайте <span class="gold">или напишите</span></h2><p class="lead">Подберём электровелосипед под ваши задачи и при необходимости доставим по удобному адресу.</p></div>
<div class="loc-grid"><div class="panel loc-card rv"><div class="loc-tabs" role="tablist"></div>
<div class="loc-item">{ic('pin')}<div><span>Адрес</span><b data-loc="addr">{ADDR}</b></div></div>
<div class="loc-item">{ic('phone')}<div><span>Телефон</span><b><a href="{TEL}">{PHONE}</a></b></div></div>
<div class="loc-btns"><a class="btn btn-gold btn-block" data-loc="route" href="{POINTS[0]['route']}" target="_blank" rel="noopener">{ic('route')}Построить маршрут в 2ГИС</a>
<a class="btn btn-ghost btn-block" href="{TEL}">{ic('phone')}Позвонить</a>
<a class="btn btn-ghost btn-block" href="{WA}" target="_blank" rel="noopener">{ic('wa')}Написать в WhatsApp</a>
<a class="btn btn-ghost btn-block" href="{TG}" target="_blank" rel="noopener">{ic('tg')}Написать в Telegram</a></div></div>
<div class="map-wrap rv d1"><div id="map"></div><div class="map-ph">Загружаем карту 2ГИС…</div></div></div></div></section>
<script>window.VOLT_POINTS={pts};</script>'''

def cta_block(p):
    return f'''<section class="section" style="padding-top:0"><div class="container"><div class="cta rv"><img class="cta-mark" src="{p}img/brand/mark.svg" alt=""><div class="cta-grid">
<div><span class="eyebrow">Пишите или звоните</span><h2 style="margin-top:14px">Полностью <span class="gold">готовы к работе</span></h2><p class="lead">Новая техника · Без залога · Собственный сервис · Аренда с выкупом</p></div>
<div><a class="phone-big" href="{TEL}">{PHONE}</a><p style="color:var(--muted);margin-bottom:18px">{ADDR}</p><div class="btns"><a class="btn btn-gold" href="{TEL}">{ic('phone')}Позвонить</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ic('wa')}Написать в WhatsApp</a><a class="btn btn-ghost" href="{TG}" target="_blank" rel="noopener">{ic('tg')}Написать в Telegram</a></div></div>
</div></div></div></section>'''

def index():
    p=''
    advh=''.join(f'<div class="adv rv d{i%4}{" big" if i==0 else ""}"><span class="num">0{i+1}</span><div class="ic">{ic(a)}</div><h3>{t}</h3><p>{d}</p></div>' for i,(a,t,d) in enumerate(ADV))
    cards=''.join(card(m,p,i) for i,m in enumerate(MODELS))
    mq=''.join(f'<span>{t}</span>' for t in ['Новая техника','Без залога','Собственный сервис','Аренда с выкупом','Для курьеров','Доставка по городу и области']*2)
    s=head('VOLT ONE — аренда электровелосипедов WENBOX для курьеров в Новосибирске','Новые электровелосипеды WENBOX для курьеров: аренда от 4 000 ₽ в неделю, аренда с выкупом, без залога. Собственный сервис, подменный велосипед. Новосибирск, ул. Пролетарская, 50.',p,'')
    s+=header(p,'')
    s+=f'''<main>
<section class="hero"><div class="container hero-grid">
<div class="hero-text"><div class="hero-tags rv"><span class="tag"><i></i>Аренда</span><span class="tag"><i></i>Аренда с выкупом</span><span class="tag"><i></i>Без залога</span></div>
<h1 class="rv d1">Новые электро&shy;велосипеды <span class="gold line2">для курьеров</span></h1>
<p class="lead rv d2">WENBOX в аренду и с выкупом. Все электровелосипеды новые, полностью подготовлены к работе и подходят для ежедневной работы курьером.</p>
<div class="hero-btns rv d3"><a class="btn btn-gold" href="catalog/">Выбрать модель{ic('arrow')}</a><a class="btn btn-ghost" href="{TEL}">{ic('phone')}{PHONE}</a></div>
<div class="hero-stats rv d3"><div><b>от 4 000 ₽</b><span>аренда в неделю</span></div><div><b>0 ₽</b><span>залог</span></div><div><b>до 70 км/ч</b><span>скорость U2 / U2 PRO</span></div></div></div>
<div class="hero-media rv d2"><div class="hero-photo"><picture><source srcset="img/hero.webp" type="image/webp"><img src="img/hero.jpg" alt="Электровелосипеды WENBOX U2 с брендингом VOLT ONE" fetchpriority="high"></picture>
<div class="cap"><div><b>WENBOX U2 / U2 PRO</b>Реальное фото нашего парка</div></div></div>
<div class="float-chip chip-1">{ic('shield')}<div><b>Без залога</b><span>новая техника</span></div></div>
<div class="float-chip chip-2">{ic('wrench')}<div><b>Свой сервис</b><span>подменный — бесплатно</span></div></div></div>
</div></section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section" id="adv"><div class="container"><div class="section-head rv"><span class="eyebrow">Почему выбирают нас</span><h2>Всё, чтобы вы <span class="gold">работали, а не чинились</span></h2></div>
<div class="adv-grid">{advh}</div></div></section>

<section class="section" id="models" style="padding-top:0"><div class="container"><div class="section-head row rv"><div style="display:flex;flex-direction:column;gap:16px"><span class="eyebrow">Модели WENBOX</span><h2>Выберите <span class="gold">свой электровелосипед</span></h2></div>{seg('#models-grid')}</div>
<div class="models four mode-rent" id="models-grid">{cards}</div>
<div class="center mt-40 rv"><a class="btn btn-ghost" href="catalog/">{ic('grid')}Весь каталог</a></div></div></section>

<section class="section" id="kit" style="padding-top:0"><div class="container"><div class="section-head rv"><span class="eyebrow">Комплектация</span><h2>Соберите <span class="gold">под свою работу</span></h2></div>
<div class="kit-grid"><div class="panel rv"><h3>На выбор — к любой модели</h3><p>Кофр, двойная сидушка или багажник: выберите, что нужно для ваших заказов.</p>
<div class="opt-list three"><div class="opt">{ic('bag')}<b>Кофр</b></div><div class="opt">{ic('seat')}<b>Двойная сидушка</b></div><div class="opt">{ic('rack')}<b>Багажник</b></div></div></div>
<div class="panel rv d1"><h3>Уже входит в стоимость</h3><p>Без доплат — всё, что нужно в первый же рабочий день.</p>
<div class="inc-list"><div class="inc">{ic('mobile')}Держатель для телефона<span class="ok">включено</span></div><div class="inc">{ic('plug')}Зарядное устройство<span class="ok">включено</span></div><div class="inc">{ic('alarm')}Сигнализация<span class="ok">включено</span></div></div></div></div></div></section>

<section class="section service" id="service"><div class="container service-grid">
<div class="rv"><span class="eyebrow">Сервис</span><h2 style="margin:16px 0">Собственный сервис <span class="gold">и подменный велосипед</span></h2><p class="lead">Быстрое обслуживание и ремонт. Если ремонт занимает больше времени, бесплатно предоставляем подменный электровелосипед.</p>
<div class="couriers"><p>Отлично подходят для курьеров:</p><div class="chips"><span>Яндекс Еда</span><span>Самокат</span><span>Купер</span><span>и др.</span></div></div></div>
<div class="srv-list"><div class="srv rv">{'<div class="ic">'+ic('wrench')+'</div>'}<div><h3>Быстрое обслуживание и ремонт</h3><p>Свой сервис — не нужно искать мастерскую и ждать очередь.</p></div></div>
<div class="srv rv d1"><div class="ic">{ic('swap')}</div><div><h3>Подменный электровелосипед бесплатно</h3><p>Если ремонт занимает больше времени — вы продолжаете работать.</p></div></div>
<div class="srv rv d2"><div class="ic">{ic('truck')}</div><div><h3>Доставка в отдалённые районы</h3><p>Доставляем электровелосипеды в отдалённые районы города и области.</p></div></div></div>
</div></section>

<section class="section" id="steps"><div class="container"><div class="section-head rv"><span class="eyebrow">Как начать</span><h2>Четыре шага <span class="gold">до первого заказа</span></h2></div>
<div class="steps"><div class="step rv"><span class="n">01</span><h3>Позвоните или напишите</h3><p>{PHONE} — звонок, WhatsApp или Telegram.</p></div>
<div class="step rv d1"><span class="n">02</span><h3>Подберём модель</h3><p>Подберём электровелосипед под ваши задачи: аренда или аренда с выкупом.</p></div>
<div class="step rv d2"><span class="n">03</span><h3>Выберите комплектацию</h3><p>Кофр, двойная сидушка или багажник — на выбор.</p></div>
<div class="step rv d3"><span class="n">04</span><h3>Заберите или получите доставкой</h3><p>На Пролетарской, 50 или доставим по удобному адресу.</p></div></div></div></section>
{cta_block(p)}
{contacts_block()}
</main>'''
    s+=footer(p)
    return s

def catalog():
    p='../'
    cards=''.join(card(m,p,i) for i,m in enumerate(MODELS))
    s=head('Каталог электровелосипедов WENBOX — VOLT ONE','Модели WENBOX U2 / U2 PRO, U2 BIG, U5, R9: характеристики, цены аренды и аренды с выкупом. Без залога. Новосибирск.',p,'catalog/')
    s+=header(p,'catalog',True)
    s+=f'''<main><section class="phero"><div class="container"><div class="crumbs"><a href="../">Главная</a><i>/</i><span>Каталог</span></div>
<div class="section-head row" style="margin-bottom:0"><div style="display:flex;flex-direction:column;gap:16px"><span class="eyebrow">Каталог</span><h1 style="font-size:clamp(32px,6vw,60px)">Электровелосипеды <span class="gold">WENBOX</span></h1><p class="lead">Все модели новые и полностью готовы к работе. Без залога. Комплектация на выбор: кофр, двойная сидушка, багажник.</p></div>{seg('#models-grid')}</div></div></section>
<section class="section" style="padding-top:30px"><div class="container"><div class="models mode-rent" id="models-grid">{cards}</div></div></section>
{cta_block(p)}</main>'''
    s+=footer(p)
    return s

def model_page(m):
    p='../../'
    ph=photos(m['slug'])
    if ph:
        imgs=[p+x[:-5]+'.jpg' for x in ph]
        imgs_w=[p+x for x in ph]
        nav=(f'<button class="gal-nav gal-prev" data-gal="-1" aria-label="Предыдущее фото">{ic("left")}</button><button class="gal-nav gal-next" data-gal="1" aria-label="Следующее фото">{ic("right")}</button><span class="gal-count">1 / {len(ph)}</span>' if len(ph)>1 else '')
        gal=f'''<div class="gallery-main" data-imgs='{json.dumps(imgs_w)}'><picture><img src="{imgs_w[0]}" alt="{m['name']} — фото"></picture>{nav}</div>'''
        if len(ph)>1: gal+='<div class="thumbs">'+''.join(f'<button class="{"on" if k==0 else ""}" aria-label="Фото {k+1}"><img src="{u}" alt="" loading="lazy"></button>' for k,u in enumerate(imgs_w))+'</div>'
        gal+=f'<div class="lb"><button class="lb-close" aria-label="Закрыть">{ic("x")}</button><button class="gal-nav gal-prev" data-gal="-1" aria-label="Назад">{ic("left")}</button><img src="" alt="{m["name"]}"><button class="gal-nav gal-next" data-gal="1" aria-label="Вперёд">{ic("right")}</button></div>'
        og=ph[0][:-5]+'.jpg'
    else:
        gal=f'<div class="gallery-main noimg"><div class="ph">{BIKE_SVG}<small>Фото скоро</small></div></div>'; og='img/og.jpg'
    rent,buy=price_block(m)
    spec=''.join(f'<div><span>{k}</span><b>{v}{(" · "+e) if e else ""}</b></div>' for _,k,v,e in m['specs'])
    spec+='<div><span>Комплектация на выбор</span><b>Кофр, двойная сидушка, багажник</b></div><div><span>Входит в стоимость</span><b>Держатель для телефона, зарядное устройство, сигнализация</b></div>'
    desc=''.join(f'<p class="lead" style="margin-bottom:12px">{x}</p>' for x in m['desc'])
    others=''.join(card(o,p,i) for i,o in enumerate([x for x in MODELS if x is not m]))
    pr=min(v for _,v in m['rent'])
    s=head(f'{m["name"]} — аренда от {pr:,} ₽/нед | VOLT ONE'.replace(',', ' '),f'{m["name"]}: '+', '.join(f'{k} {v}' for _,k,v,_ in m['specs'])+'. Аренда'+(' и аренда с выкупом' if m['buy'] else '')+', без залога. Новосибирск.',p,f'catalog/{m["slug"]}/',og)
    s+=header(p,'catalog',True)
    s+=f'''<main><section class="phero" style="padding-bottom:0"><div class="container"><div class="crumbs"><a href="{p}">Главная</a><i>/</i><a href="{p}catalog/">Каталог</a><i>/</i><span>{m['name']}</span></div>
<div class="prod"><div class="rv">{gal}</div>
<div class="prod-info rv d1"><div class="hero-tags" style="margin-bottom:0"><span class="tag"><i></i>Новая</span><span class="tag"><i></i>Без залога</span>{'<span class="tag"><i></i>Выкуп</span>' if m['buy'] else ''}</div>
<h1>{m['name']}</h1>{desc}<div style="height:12px"></div>
<div class="spec-table">{spec}</div>
<div class="tariffs"><div class="tariff hl"><h4>{ic('clock')}Обычная аренда</h4>{rent}</div><div class="tariff"><h4>{ic('key')}Аренда с выкупом</h4>{buy}</div></div>
<div class="prod-btns"><a class="btn btn-gold" href="{TEL}">{ic('phone')}Позвонить</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ic('wa')}Написать в WhatsApp</a><a class="btn btn-ghost full" href="{TG}" target="_blank" rel="noopener">{ic('tg')}Написать в Telegram</a></div>
<p class="note">Подберём электровелосипед под ваши задачи и при необходимости доставим по удобному адресу.</p></div></div></div></section>
<section class="section"><div class="container"><div class="section-head rv"><span class="eyebrow">Другие модели</span><h2>Смотрите <span class="gold">также</span></h2></div><div class="models mode-rent" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{others}</div></div></section>
{cta_block(p)}</main>'''
    s+=footer(p)
    return s

def w(path,txt):
    path=os.path.join(ROOT,path); os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w').write(txt)
w('index.html',index()); w('catalog/index.html',catalog())
for m in MODELS: w(f'catalog/{m["slug"]}/index.html',model_page(m))
w('404.html',head('Страница не найдена — VOLT ONE','',SITE_URL,'')+f'<main><section class="phero"><div class="container"><h1>Страница <span class="gold">не найдена</span></h1><p class="lead" style="margin:20px 0 30px">Перейдите на главную или в каталог.</p><a class="btn btn-gold" href="{SITE_URL}">На главную</a></div></section></main></body></html>')
print('built', {m['slug']:len(photos(m['slug'])) for m in MODELS})
