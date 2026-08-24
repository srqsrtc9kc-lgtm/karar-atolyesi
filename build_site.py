from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from content_data import ARTICLES


ROOT = Path(__file__).resolve().parent
SITE_URL = "https://srqsrtc9kc-lgtm.github.io/karar-atolyesi"
PUBLISHED = "24 Ağustos 2026"


STYLE = r"""
:root {
  --ink: #17211d;
  --paper: #f3efe4;
  --card: #fffdf7;
  --line: #cec5b2;
  --green: #176b4a;
  --green-dark: #0d4b35;
  --yellow: #f2c95c;
  --muted: #68655c;
  --max: 1120px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 17px/1.68 Georgia, "Times New Roman", serif;
}
a { color: var(--green-dark); text-underline-offset: 3px; }
a:hover { color: var(--green); }
.skip { position: absolute; left: -9999px; }
.skip:focus { left: 12px; top: 12px; z-index: 99; background: white; padding: 10px; }
.topbar { border-bottom: 1px solid var(--line); background: rgba(243,239,228,.96); }
.nav {
  max-width: var(--max); margin: auto; min-height: 72px; padding: 0 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 24px;
}
.brand { color: var(--ink); text-decoration: none; font: 800 20px/1 system-ui, sans-serif; letter-spacing: -.03em; }
.brand-mark { display: inline-grid; place-items: center; width: 28px; height: 28px; margin-right: 7px; border-radius: 50%; background: var(--green); color: white; }
.nav-links { display: flex; gap: 20px; flex-wrap: wrap; font: 700 13px/1.2 system-ui, sans-serif; }
.nav-links a { color: var(--ink); text-decoration: none; }
.wrap { max-width: var(--max); margin: auto; padding: 0 24px; }
.hero { padding: 76px 0 54px; border-bottom: 3px solid var(--ink); }
.eyebrow { color: var(--green); font: 800 12px/1.2 system-ui, sans-serif; letter-spacing: .15em; text-transform: uppercase; }
h1 { max-width: 930px; margin: 18px 0; font-size: clamp(48px, 9vw, 104px); line-height: .9; letter-spacing: -.07em; }
.lead { max-width: 760px; margin: 0; font-size: clamp(20px, 2.5vw, 27px); line-height: 1.45; }
.principles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; margin: 34px 0 0; border: 1px solid var(--line); background: var(--line); }
.principle { padding: 22px; background: var(--card); }
.principle strong { display: block; margin-bottom: 7px; font: 800 14px/1.2 system-ui, sans-serif; }
.section-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin: 58px 0 22px; }
.section-head h2 { margin: 0; font-size: clamp(30px, 5vw, 50px); line-height: 1; letter-spacing: -.045em; }
.section-head p { max-width: 440px; margin: 0; color: var(--muted); }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; padding-bottom: 70px; }
.card { display: flex; flex-direction: column; min-height: 310px; padding: 28px; border: 1px solid var(--line); background: var(--card); text-decoration: none; color: var(--ink); transition: transform .15s ease, box-shadow .15s ease; }
.card:hover { color: var(--ink); transform: translateY(-3px); box-shadow: 0 12px 25px rgba(23,33,29,.09); }
.card .meta { color: var(--green); font: 800 11px/1.2 system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; }
.card h3 { margin: 34px 0 14px; font-size: clamp(25px, 3vw, 36px); line-height: 1.05; letter-spacing: -.035em; }
.card p { margin: 0 0 24px; color: #484b45; }
.card .read { margin-top: auto; font: 800 13px/1.2 system-ui, sans-serif; }
.article-shell { max-width: 820px; margin: auto; padding: 48px 24px 90px; }
.crumbs { margin-bottom: 44px; color: var(--muted); font: 650 13px/1.3 system-ui, sans-serif; }
.article-head { padding-bottom: 30px; border-bottom: 3px solid var(--ink); }
.article-head h1 { max-width: 820px; margin: 16px 0 22px; font-size: clamp(42px, 8vw, 78px); line-height: .95; }
.article-head .summary { font-size: 22px; line-height: 1.48; }
.article-meta { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 24px; color: var(--muted); font: 650 12px/1.3 system-ui, sans-serif; }
.notice { margin: 30px 0; padding: 18px 20px; border-left: 5px solid var(--green); background: #e3ede6; font-size: 15px; }
.article-body h2 { margin: 52px 0 12px; font-size: 34px; line-height: 1.1; letter-spacing: -.035em; }
.article-body h3 { margin: 32px 0 8px; font-size: 23px; line-height: 1.2; }
.article-body p { margin: 0 0 18px; }
.article-body ul, .article-body ol { margin: 10px 0 24px; padding-left: 25px; }
.article-body li { margin-bottom: 9px; }
.checklist { margin: 32px 0; padding: 22px 26px; border: 1px solid var(--line); background: var(--card); }
.checklist strong { font: 800 15px/1.2 system-ui, sans-serif; }
.next { margin-top: 58px; padding-top: 26px; border-top: 1px solid var(--line); }
.page { max-width: 780px; min-height: 65vh; padding: 60px 24px 90px; }
.page h1 { font-size: clamp(44px, 8vw, 74px); }
.page h2 { margin-top: 40px; font-size: 30px; }
.footer { border-top: 1px solid var(--line); background: var(--card); }
.footer-inner { max-width: var(--max); margin: auto; padding: 34px 24px 46px; display: flex; justify-content: space-between; gap: 24px; flex-wrap: wrap; color: var(--muted); font: 13px/1.6 system-ui, sans-serif; }
.footer-links { display: flex; gap: 16px; flex-wrap: wrap; }
@media (max-width: 760px) {
  .nav { align-items: flex-start; padding-top: 20px; padding-bottom: 20px; flex-direction: column; }
  .hero { padding-top: 52px; }
  .principles, .grid { grid-template-columns: 1fr; }
  .section-head { align-items: flex-start; flex-direction: column; }
  .card { min-height: 260px; }
}
@media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; transition: none !important; } }
"""


def nav(prefix: str = "") -> str:
    return f"""
<a class="skip" href="#icerik">İçeriğe geç</a>
<header class="topbar"><nav class="nav" aria-label="Ana menü">
  <a class="brand" href="{prefix}index.html"><span class="brand-mark">K</span>Karar Atölyesi</a>
  <div class="nav-links">
    <a href="{prefix}index.html#rehberler">Rehberler</a>
    <a href="{prefix}hakkimizda.html">Hakkımızda</a>
    <a href="{prefix}seffaflik.html">Şeffaflık</a>
  </div>
</nav></header>"""


def footer(prefix: str = "") -> str:
    return f"""
<footer class="footer"><div class="footer-inner">
  <div><strong>Karar Atölyesi</strong><br>Bağımsız ve ücretsiz Türkçe seçim rehberleri.</div>
  <div class="footer-links">
    <a href="{prefix}hakkimizda.html">Hakkımızda</a>
    <a href="{prefix}seffaflik.html">Şeffaflık</a>
    <a href="{prefix}gizlilik.html">Gizlilik</a>
  </div>
</div></footer>"""


def layout(title: str, description: str, body: str, *, prefix: str = "", canonical: str = "") -> str:
    canonical_tag = f'<link rel="canonical" href="{html.escape(canonical)}">' if canonical else ""
    return f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description)}">
  <meta name="color-scheme" content="light">
  {canonical_tag}
  <link rel="stylesheet" href="{prefix}style.css">
  <title>{html.escape(title)} · Karar Atölyesi</title>
</head>
<body>
{nav(prefix)}
{body}
{footer(prefix)}
</body>
</html>
"""


def article_page(article: dict[str, str], index: int) -> str:
    next_article = ARTICLES[index + 1] if index + 1 < len(ARTICLES) else ARTICLES[0]
    body = f"""
<main id="icerik" class="article-shell">
  <div class="crumbs"><a href="../index.html">Ana sayfa</a> / {html.escape(article['category'])}</div>
  <header class="article-head">
    <div class="eyebrow">{html.escape(article['category'])} · Rehber {index + 1:02d}</div>
    <h1>{html.escape(article['title'])}</h1>
    <p class="summary">{html.escape(article['summary'])}</p>
    <div class="article-meta"><span>Yayın: {PUBLISHED}</span><span>{html.escape(article['read_time'])}</span><span>Reklamsız rehber</span></div>
  </header>
  <aside class="notice"><strong>Şeffaflık notu:</strong> Bu sayfada şu anda gelir ortaklığı bağlantısı yoktur. İleride eklenirse bağlantının niteliği açıkça işaretlenir; komisyon ihtimali editoryal ölçütleri değiştirmez.</aside>
  <article class="article-body">{article['body']}</article>
  <div class="next"><span class="eyebrow">Sıradaki rehber</span><h2><a href="{next_article['slug']}.html">{html.escape(next_article['title'])}</a></h2></div>
</main>"""
    return layout(
        article["title"],
        article["summary"],
        body,
        prefix="../",
        canonical=f"{SITE_URL}/rehberler/{article['slug']}.html",
    )


def build() -> None:
    article_dir = ROOT / "rehberler"
    article_dir.mkdir(exist_ok=True)
    (ROOT / "style.css").write_text(STYLE.strip() + "\n", encoding="utf-8")

    cards = "\n".join(
        f"""<a class="card" href="rehberler/{a['slug']}.html">
  <span class="meta">{html.escape(a['category'])} · {i:02d}</span>
  <h3>{html.escape(a['title'])}</h3>
  <p>{html.escape(a['summary'])}</p>
  <span class="read">Rehberi oku →</span>
</a>"""
        for i, a in enumerate(ARTICLES, start=1)
    )
    index_body = f"""
<main id="icerik" class="wrap">
  <section class="hero">
    <div class="eyebrow">Bağımsız seçim rehberleri</div>
    <h1>Daha çok değil, daha doğru seç.</h1>
    <p class="lead">Günlük ürünleri gösterişsiz ölçütlerle değerlendiren ücretsiz Türkçe rehberler. Önce ihtiyacı tanımlar, sonra gereksiz masrafı eleriz.</p>
    <div class="principles" aria-label="Yayın ilkeleri">
      <div class="principle"><strong>İhtiyaç önce gelir</strong>Özellik kalabalığı yerine kullanım senaryosunu netleştiririz.</div>
      <div class="principle"><strong>Değişken bilgi işaretlenir</strong>Fiyat, stok ve model ayrıntıları satın alma anında yeniden kontrol edilir.</div>
      <div class="principle"><strong>Bağlantı şeffaftır</strong>Gelir ortaklığı bağlantısı varsa okuyucu görmeden önce açıkça belirtilir.</div>
    </div>
  </section>
  <section id="rehberler" aria-labelledby="rehber-baslik">
    <div class="section-head"><h2 id="rehber-baslik">10 başlangıç rehberi</h2><p>Karşılaştırmaya başlamadan önce doğru soruları sormak için hazırlanmış, ürün bağımsız kontrol listeleri.</p></div>
    <div class="grid">{cards}</div>
  </section>
</main>"""
    (ROOT / "index.html").write_text(
        layout("Ana sayfa", "Günlük ürünler için bağımsız ve ücretsiz Türkçe seçim rehberleri.", index_body, canonical=f"{SITE_URL}/"),
        encoding="utf-8",
    )

    for index, article in enumerate(ARTICLES):
        (article_dir / f"{article['slug']}.html").write_text(article_page(article, index), encoding="utf-8")

    about = f"""<main id="icerik" class="wrap page"><div class="eyebrow">Yayın hakkında</div><h1>Hakkımızda</h1>
<p class="lead">Karar Atölyesi, günlük ürünlerde karar vermeyi kolaylaştırmak için kurulan bağımsız bir Türkçe rehber yayınıdır.</p>
<h2>Ne yapıyoruz?</h2><p>Bir ürünü övmek yerine önce kullanım senaryosunu, toplam maliyeti, bakım ihtiyacını ve iade riskini inceleriz. Rehberlerimiz ürün bağımsız ölçütler verir; fiyat, stok ve model gibi değişebilen bilgiler satın alma anında yeniden doğrulanmalıdır.</p>
<h2>Nasıl hazırlanıyor?</h2><p>İçerikler araştırma, taslak, editoryal kontrol ve şeffaflık kontrolünden geçer. Bir ürünü fiziksel olarak denemediğimiz sürece denediğimizi söylemeyiz. Sponsorlu yerleşim editoryal sıralamayı satın alamaz.</p>
<h2>İletişim</h2><p>Bu ilk sürümde iletişim formu ve veri toplama bulunmuyor. Kamuya açık iletişim kanalı eklendiğinde bu sayfada duyurulacaktır.</p></main>"""
    (ROOT / "hakkimizda.html").write_text(layout("Hakkımızda", "Karar Atölyesi'nin amacı ve yayın yöntemi.", about, canonical=f"{SITE_URL}/hakkimizda.html"), encoding="utf-8")

    transparency = f"""<main id="icerik" class="wrap page"><div class="eyebrow">Editoryal ilke</div><h1>Şeffaflık</h1>
<p class="lead">Okurun hangi bilginin editoryal, hangi bağlantının ticari olduğunu ilk bakışta anlayabilmesi gerekir.</p>
<h2>Mevcut durum</h2><p>Bu sitede şu anda gelir ortaklığı bağlantısı, sponsorlu yerleşim veya ücretli ürün tanıtımı yoktur. Site bir mağaza değildir; sipariş veya ödeme almaz.</p>
<h2>İleride bağlantı eklenirse</h2><p>Gelir ortaklığı bağlantıları içerik başında ve bağlantının yakınında açıkça belirtilir. Komisyon oranı, bir ürünün değerlendirme ölçütünü veya eleştiri hakkımızı değiştirmez. Uygun olmayan ürün yalnız gelir ihtimali nedeniyle önerilmez.</p>
<h2>Düzeltmeler</h2><p>Yanlış veya eskimiş bilgi tespit edildiğinde içerik güncellenir ve önemli değişiklikler sayfada açıklanır. Fiyat ve stok gibi hızlı değişen bilgiler için kesinlik iddiasında bulunulmaz.</p></main>"""
    (ROOT / "seffaflik.html").write_text(layout("Şeffaflık", "Karar Atölyesi gelir ortaklığı ve editoryal bağımsızlık ilkeleri.", transparency, canonical=f"{SITE_URL}/seffaflik.html"), encoding="utf-8")

    privacy = f"""<main id="icerik" class="wrap page"><div class="eyebrow">Veri politikası</div><h1>Gizlilik</h1>
<p class="lead">Bu ilk sürüm olabildiğince az veriyle çalışır.</p>
<h2>Toplanan veriler</h2><p>Sitede üyelik, yorum, iletişim formu, ödeme, reklam çerezi veya ziyaretçi analitiği yoktur. Karar Atölyesi doğrudan kişisel veri istemez ve saklamaz.</p>
<h2>Barındırma</h2><p>Site GitHub Pages üzerinde sunulur. Barındırma hizmetinin güvenlik ve işletim kayıtları kendi politikalarına tabi olabilir. Ayrıntılar için GitHub'ın yürürlükteki gizlilik bildirimine bakılmalıdır.</p>
<h2>Değişiklik</h2><p>Analitik, iletişim veya başka bir veri işleme özelliği eklenmeden önce bu sayfa güncellenir; gerekli onay ve bilgilendirme mekanizmaları kurulmadan özellik etkinleştirilmez.</p></main>"""
    (ROOT / "gizlilik.html").write_text(layout("Gizlilik", "Karar Atölyesi veri ve gizlilik yaklaşımı.", privacy, canonical=f"{SITE_URL}/gizlilik.html"), encoding="utf-8")

    not_found = """<main id="icerik" class="wrap page"><div class="eyebrow">404</div><h1>Bu sayfa bulunamadı.</h1><p class="lead">Bağlantı değişmiş olabilir. <a href="index.html">Ana sayfadaki rehberlere dön.</a></p></main>"""
    (ROOT / "404.html").write_text(layout("Sayfa bulunamadı", "Aradığınız sayfa bulunamadı.", not_found), encoding="utf-8")

    urls = [f"{SITE_URL}/", f"{SITE_URL}/hakkimizda.html", f"{SITE_URL}/seffaflik.html", f"{SITE_URL}/gizlilik.html"]
    urls.extend(f"{SITE_URL}/rehberler/{a['slug']}.html" for a in ARTICLES)
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
    sitemap += "\n".join(f"  <url><loc>{html.escape(url)}</loc></url>" for url in urls)
    sitemap += "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


def validate() -> None:
    expected = [ROOT / "index.html", ROOT / "style.css", ROOT / "sitemap.xml", ROOT / "robots.txt"]
    expected.extend(ROOT / "rehberler" / f"{a['slug']}.html" for a in ARTICLES)
    missing = [str(path.relative_to(ROOT)) for path in expected if not path.exists()]
    if missing:
        raise SystemExit(f"Eksik dosyalar: {', '.join(missing)}")
    if len(ARTICLES) < 10:
        raise SystemExit("En az 10 özgün rehber gerekir")
    forbidden = [r"@gmail\.com", r"password\s*[:=]", r"credential\s*[:=]", r"secret\s*[:=]", r"api[_-]?key\s*[:=]", r"BEGIN [A-Z ]*PRIVATE KEY"]
    public_files = list(ROOT.glob("*.html")) + list((ROOT / "rehberler").glob("*.html")) + [ROOT / "style.css"]
    for path in public_files:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            if re.search(pattern, text, re.IGNORECASE):
                raise SystemExit(f"Güvenlik taraması başarısız: {path.name}")
        premature_claim = "Amazon " + "Gelir Ortağı olarak"
        if premature_claim in text:
            raise SystemExit("Amazon hesabı açılmadan ortaklık beyanı yayımlanamaz")
    print(f"OK: {len(ARTICLES)} rehber, {len(public_files)} genel dosya, sır taraması temiz")


if __name__ == "__main__":
    if "--check" not in sys.argv:
        build()
    validate()
