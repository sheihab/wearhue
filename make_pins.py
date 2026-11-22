"""Generates Wearhue Pinterest pins (1000x1500 PNG) into ./pins/ plus pinterest-bulk.csv.
Run: python3 make_pins.py   (needs: pip install playwright && playwright install chromium)"""
import asyncio, csv, os, datetime
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sheihab.github.io/wearhue/"
BOARD_SKIN = "Colours for your skin tone"
BOARD_MATCH = "What colours go together"
START = datetime.datetime(2026, 11, 23, 8, 0)   # 08:00 UTC = 7pm Sydney; one pin per day

SK = {"fair":"#EECDB6","medium":"#C08A63","olive":"#B08A5E","dark":"#5A3825"}
PG = {"fair":"best-colours-for-fair-skin.html","medium":"best-colours-for-medium-skin.html",
      "olive":"best-colours-for-medium-skin.html","dark":"best-colours-for-dark-skin.html"}

# (file, top line, big line, subtitle, skin-chip colour, colours, link page, board, title, description, keywords)
PINS = []
def grid(fn, a, b, sub, chip, cols, page, board, title, desc, kw):
    PINS.append(dict(kind="grid", fn=fn, a=a, b=b, sub=sub, chip=chip, cols=cols, page=page, board=board, title=title, desc=desc, kw=kw))
def pairs(fn, a, b, sub, rows, page, board, title, desc, kw):
    PINS.append(dict(kind="pairs", fn=fn, a=a, b=b, sub=sub, rows=rows, page=page, board=board, title=title, desc=desc, kw=kw))

# --- skin tone x undertone palettes
SKIN_PALS = [
 ("dark","warm","Best colours for","warm dark skin","Golden undertone · gold jewellery",[("#FFB703","Saffron"),("#FB8500","Tangerine"),("#D62828","Tomato red"),("#2A9D8F","Teal"),("#6A994E","Leaf green"),("#9B2226","Oxblood"),("#C9A227","Old gold"),("#FFF3E0","Warm white"),("#F4A261","Apricot")]),
 ("dark","cool","Best colours for","cool dark skin","Blue or ashy undertone · silver jewellery",[("#0047AB","Cobalt"),("#FF1493","Hot pink"),("#00A86B","Jade"),("#7B2CBF","Violet"),("#DC143C","Crimson"),("#00B4D8","Cyan"),("#FFFFFF","Crisp white"),("#4361EE","Royal blue"),("#800080","Purple")]),
 ("dark","neutral","Best colours for","dark brown skin","Bright, rich colours make deep skin glow",[("#E63946","Red"),("#FFB703","Sun yellow"),("#3A86FF","Bright blue"),("#8338EC","Violet"),("#06D6A0","Mint"),("#FF006E","Pink"),("#FFFFFF","White"),("#2A9D8F","Teal"),("#FB5607","Orange")]),
 ("medium","warm","Best colours for","warm medium skin","Golden undertone · tans easily",[("#E07A5F","Terracotta"),("#F2A541","Marigold"),("#6B8E23","Olive"),("#2A9D8F","Teal"),("#C1440E","Rust"),("#E9C46A","Mustard"),("#9C6644","Cinnamon"),("#F1E3C8","Cream"),("#BC4749","Brick")]),
 ("medium","cool","Best colours for","cool medium skin","Rosy undertone · silver jewellery",[("#0F52BA","Sapphire"),("#50C878","Emerald"),("#8E44AD","Purple"),("#E0115F","Ruby"),("#4682B4","Steel blue"),("#DE5D83","Blush"),("#008080","Teal"),("#FFFFFF","White"),("#1F2A44","Navy")]),
 ("olive","neutral","Best colours for","olive skin","Earth & jewel tones are your sweet spot",[("#6B8E23","Olive"),("#E07A5F","Terracotta"),("#800020","Burgundy"),("#2A9D8F","Teal"),("#50C878","Emerald"),("#E9C46A","Mustard"),("#F1E3C8","Cream"),("#1F2A44","Navy"),("#C19A6B","Camel")]),
 ("fair","warm","Best colours for","warm fair skin","Peachy undertone · freckles & gold",[("#F28C6B","Coral"),("#F4A68C","Peach"),("#A8B26A","Pistachio"),("#5BAE9C","Turquoise"),("#C7714E","Terracotta"),("#E7C27D","Wheat"),("#C19A6B","Camel"),("#F3E7D3","Ivory"),("#2F3B59","Soft navy")]),
 ("fair","cool","Best colours for","cool pale skin","Pink undertone · burns easily",[("#7FA7D9","Powder blue"),("#E6A8C3","Rose pink"),("#9C89B8","Lavender"),("#3E7CB1","Sapphire"),("#C94C7C","Raspberry"),("#7DB7A5","Jade mint"),("#B8577E","Berry"),("#2E3A59","Navy"),("#A9A9B3","Dove grey")]),
 ("fair","neutral","Best colours for","fair neutral skin","Soft, muted shades never overpower",[("#E8A0A0","Dusty rose"),("#8FBC8F","Sage"),("#6C8EBF","Soft blue"),("#F4C095","Apricot"),("#5F9EA0","Teal grey"),("#D6A2AD","Mauve"),("#B39DDB","Soft violet"),("#F5F0E8","Off-white"),("#2F3E46","Slate")]),
]
KW_SKIN = {"dark":"colours for dark skin, colors for brown skin, best colours for black skin, dark skin outfits",
           "medium":"colours for medium skin, colours for tan skin, medium skin tone outfits",
           "olive":"colours for olive skin, olive skin tone outfits, what colours suit olive skin",
           "fair":"colours for pale skin, colours for fair skin, pale skin outfits"}
for skin,und,a,b,sub,cols in SKIN_PALS:
    nice = b
    grid(f"{skin}-{und}-skin-palette", a, b, sub, SK[skin], cols, PG[skin], BOARD_SKIN,
         f"Best colours for {nice} – clothing colour palette",
         f"The clothing colours that suit {nice}: {', '.join(n for _,n in cols[:6]).lower()} and more. Save this palette for your next shop, then find your exact colours free in 30 seconds with Wearhue. No sign-up.",
         f"{KW_SKIN[skin]}, {und} undertone colours, colour analysis, colour palette, what colours suit me")

# --- avoid pins
for skin,label,cols in [
 ("dark","dark & brown skin",[("#8B6B4A","Mid brown"),("#A0A0A0","Mid grey"),("#C2B280","Khaki"),("#7A6A53","Dull olive"),("#E6E6FA","Pale lilac"),("#DCC7AA","Nude")]),
 ("fair","pale skin",[("#000000","Harsh black"),("#CCFF00","Neon lime"),("#FF6600","Neon orange"),("#F3D9C6","Nude"),("#FFFF66","Lemon"),("#D8C3A5","Beige")]),
 ("olive","olive skin",[("#FFFF99","Pale yellow"),("#D8C3A5","Beige"),("#CCFF00","Neon lime"),("#A7A9AC","Cool grey"),("#F0E68C","Khaki"),("#FFB6C1","Baby pink")])]:
    grid(f"colours-to-avoid-{skin}-skin", "Colours to avoid", f"with {label}", "They wash you out. Wear them away from your face", SK[skin], cols, PG[skin], BOARD_SKIN,
         f"Colours to avoid with {label} (and what to wear instead)",
         f"Some colours blend into {label} or drain your face: {', '.join(n for _,n in cols[:4]).lower()}. Wear them as trousers or shoes instead, and find the colours that actually suit you free with Wearhue.",
         f"colours to avoid {skin} skin, {KW_SKIN[skin]}, colour analysis, style tips")

# --- undertone palettes
for und,b,sub,cols in [
 ("warm","warm undertones","Earthy & golden · gold jewellery",[("#E07A5F","Terracotta"),("#E9C46A","Mustard"),("#6B8E23","Olive"),("#C1440E","Rust"),("#F28C6B","Coral"),("#2A9D8F","Teal"),("#C19A6B","Camel"),("#F1E3C8","Cream"),("#9B2226","Oxblood")]),
 ("cool","cool undertones","Jewel & blue-based · silver jewellery",[("#0F52BA","Sapphire"),("#50C878","Emerald"),("#B8577E","Berry"),("#9C89B8","Lavender"),("#E0115F","Ruby"),("#1F2A44","Navy"),("#FFFFFF","Crisp white"),("#9E9E9E","Grey"),("#008080","Teal")]),
 ("neutral","neutral undertones","Muted mid-tones · gold or silver",[("#E8A0A0","Dusty rose"),("#3C9D5D","Jade"),("#577590","Denim"),("#A23B72","Plum"),("#EDAE49","Honey"),("#5F9EA0","Teal grey"),("#F5F0E8","Soft white"),("#6A4C93","Grape"),("#2F3E46","Slate")])]:
    grid(f"{und}-undertone-palette", "Best colours for", b, sub, "#C68B59", cols, "warm-vs-cool-undertone.html", BOARD_SKIN,
         f"Best colours for {b} – clothing colour palette",
         f"Have {b}? These clothing colours flatter you most: {', '.join(n for _,n in cols[:6]).lower()}. Not sure if you're warm, cool or neutral? Take the free 30-second test on Wearhue.",
         f"{und} undertone colours, warm vs cool undertone, am I warm or cool toned, colour analysis, what colours suit me")

# --- what goes with X
GW = [
 ("navy","#1F2A44",[("#FFFFFF","White"),("#A3C4E0","Light blue"),("#C19A6B","Camel"),("#9E9E9E","Grey"),("#800020","Burgundy"),("#E6A8C3","Pink"),("#E9C46A","Mustard")]),
 ("black","#111111",[("#FFFFFF","White"),("#9E9E9E","Grey"),("#C19A6B","Camel"),("#C1121F","Red"),("#0047AB","Cobalt"),("#00875A","Emerald"),("#E8B4B8","Blush pink")]),
 ("grey","#8E8E8E",[("#1F2A44","Navy"),("#FFFFFF","White"),("#800020","Burgundy"),("#E6A8C3","Pink"),("#A3C4E0","Light blue"),("#E9C46A","Mustard"),("#2E5E4E","Forest green")]),
 ("beige","#D8C3A5",[("#FFFDF7","Cream"),("#1F2A44","Navy"),("#6F4E37","Brown"),("#111111","Black"),("#6B8E23","Olive"),("#A3C4E0","Light blue"),("#800020","Burgundy")]),
 ("olive green","#6B6B3A",[("#FFFDF7","Cream"),("#111111","Black"),("#1F2A44","Navy"),("#D8C3A5","Beige"),("#800020","Burgundy"),("#E9C46A","Mustard"),("#C1440E","Rust")]),
 ("brown","#6F4E37",[("#FFFDF7","Cream"),("#A3C4E0","Light blue"),("#D8C3A5","Beige"),("#1F2A44","Navy"),("#6B8E23","Olive"),("#C1440E","Rust"),("#E8B4B8","Pink")]),
 ("burgundy","#800020",[("#1F2A44","Navy"),("#9E9E9E","Grey"),("#FFFDF7","Cream"),("#C19A6B","Camel"),("#111111","Black"),("#6B8E23","Olive"),("#E8B4B8","Blush pink")]),
]
for name,hx,cols in GW:
    cols = cols[:6]
    slug = name.replace(" ","-")
    grid(f"what-colours-go-with-{slug}", "What colours", f"go with {name}?", f"{len(cols)} outfit combinations that always work", hx, cols,
         f"what-colours-go-with-{slug}.html", BOARD_MATCH,
         f"What colours go with {name}? {len(cols)} outfit colour combinations",
         f"What to wear with {name} clothes: {', '.join(n for _,n in cols).lower()}. Plus which shoes work and which colours to avoid. Check any colour pair on your skin tone free with Wearhue.",
         f"what colours go with {name}, what colour shirt goes with {name} pants, {name} outfit ideas, colour combinations for clothes, outfit colour matching")

# --- combos & rules (pair-row layout)
pairs("8-colour-combinations-that-always-work", "8 colour combinations", "that always work", "Save this for your next outfit",
      [("Navy","#1F2A44","White","#FFFFFF"),("Black","#111111","Camel","#C19A6B"),("Olive","#6B8E23","Cream","#F1E3C8"),("Grey","#9E9E9E","Burgundy","#800020"),
       ("Light blue","#A3C4E0","Tan","#C19A6B"),("Terracotta","#E07A5F","Denim","#577590"),("Emerald","#00875A","White","#FFFFFF"),("Pink","#E6A8C3","Grey","#9E9E9E")],
      "what-colours-go-together.html", BOARD_MATCH, "8 clothing colour combinations that always work",
      "Navy + white, black + camel, olive + cream, grey + burgundy and more: 8 outfit colour combinations that never fail. Learn the 5 simple rules for matching clothes on Wearhue.",
      "colour combinations for clothes, what colours go together, outfit colour combinations, how to match clothes, colour matching outfits")
pairs("mens-colour-combinations", "Men's outfit colour", "combinations", "Easy pairings for shirts & trousers",
      [("Navy","#1F2A44","Light blue","#A3C4E0"),("Charcoal","#36454F","White","#FFFFFF"),("Olive","#6B8E23","Navy","#1F2A44"),("Beige","#D8C3A5","Black","#111111"),
       ("Burgundy","#800020","Grey","#9E9E9E"),("Brown","#6F4E37","Light blue","#A3C4E0"),("Black","#111111","Grey","#9E9E9E"),("Camel","#C19A6B","Cream","#FFFDF7")],
      "what-colours-go-together.html", BOARD_MATCH, "Men's outfit colour combinations: shirts & trousers",
      "Easy men's colour combinations: navy + light blue, olive + navy, beige + black, burgundy + grey and more. Never guess what shirt goes with your trousers again.",
      "mens outfit colour combinations, what shirt goes with what pants, men's colour matching, mens style tips, colour combinations for clothes men")
pairs("colours-that-go-with-everything", "Colours that go", "with everything", "The 8 neutrals every wardrobe needs",
      [("White","#FFFFFF","",None),("Black","#111111","",None),("Navy","#1F2A44","",None),("Grey","#9E9E9E","",None),
       ("Beige","#D8C3A5","",None),("Camel","#C19A6B","",None),("Denim","#577590","",None),("Cream","#FFFDF7","",None)],
      "what-colours-go-together.html", BOARD_MATCH, "Colours that go with everything: 8 wardrobe neutrals",
      "White, black, navy, grey, beige, camel, denim and cream go with almost any colour. Pair one bright piece with these neutrals and your outfit always works.",
      "colours that go with everything, neutral colours clothes, capsule wardrobe colours, what colour goes with everything, wardrobe basics")
pairs("gold-or-silver-jewellery", "Gold or silver?", "Find your undertone", "The quickest undertone test there is",
      [("Gold suits you","#D4AF37","Warm undertone",None),("Silver suits you","#C0C0C0","Cool undertone",None),("Both look good","#E0B097","Neutral undertone",None),
       ("Green wrist veins","#6B8E4E","Warm",None),("Blue / purple veins","#5B6EAE","Cool",None),("Tan easily","#C68B59","Often warm",None),("Burn first","#E57373","Often cool",None)],
      "warm-vs-cool-undertone.html", BOARD_SKIN, "Gold or silver jewellery? The easy undertone test",
      "Does gold or silver suit you? It reveals your undertone: gold = warm, silver = cool, both = neutral. Plus the vein and sun tests. Take the full free undertone test on Wearhue.",
      "warm or cool undertone, gold or silver jewellery, undertone test, am I warm or cool toned, skin undertone")

HEAD = '<html><body style="margin:0"><div style="width:1000px;height:1500px;background:#F7F3EE;font-family:-apple-system,Segoe UI,Roboto,Helvetica,sans-serif;color:#1B1A19;display:flex;flex-direction:column;align-items:center;padding:86px 70px 70px;box-sizing:border-box">'
def title_html(a,b,sub):
    return (f'<div style="font-family:Iowan Old Style,Palatino,Georgia,serif;font-size:60px;line-height:1.05;text-align:center">{a}<br>'
            f'<span style="font-size:{86 if len(b)<20 else 74}px">{b}</span></div><div style="font-size:30px;color:#6F6A64;margin-top:22px;text-align:center">{sub}</div>')
FOOT = ('<div style="margin-top:40px;display:flex;flex-direction:column;align-items:center;gap:10px"><div style="background:#1B1A19;color:#fff;border-radius:999px;padding:22px 44px;font-size:32px;font-weight:600">Find your colours free →</div>'
        '<div style="font-size:26px;color:#6F6A64">sheihab.github.io/wearhue</div></div></div></body></html>')

def render(p):
    if p["kind"] == "grid":
        n = len(p["cols"]); size = 230 if n > 6 else 260
        cells = "".join(f'<div style="text-align:center"><div style="width:{size}px;height:{size}px;border-radius:32px;background:{h};position:relative;overflow:hidden;box-shadow:inset 0 0 0 2px rgba(0,0,0,.07)"><div style="position:absolute;left:50%;bottom:-70px;width:150px;height:150px;border-radius:50%;background:{p["chip"]};transform:translateX(-50%)"></div></div><div style="font-size:28px;margin-top:12px">{nm}</div></div>' for h,nm in p["cols"])
        body = f'<div style="display:grid;grid-template-columns:repeat(3,{size}px);gap:34px;margin:auto 0">{cells}</div>'
    else:
        rows = ""; many = len(p["rows"]) > 7; sq = 76 if many else 84
        for l1,h1,l2,h2 in p["rows"]:
            sw = f'<div style="display:flex"><div style="width:{sq}px;height:{sq}px;background:{h1};border-radius:{"16px 0 0 16px" if h2 else "16px"};box-shadow:inset 0 0 0 2px rgba(0,0,0,.07)"></div>' + (f'<div style="width:{sq}px;height:{sq}px;background:{h2};border-radius:0 16px 16px 0;box-shadow:inset 0 0 0 2px rgba(0,0,0,.07)"></div>' if h2 else "") + '</div>'
            txt = f'<b>{l1}</b>' + (f' + <b>{l2}</b>' if h2 else (f'<span style="color:#6F6A64"> · {l2}</span>' if l2 else ""))
            rows += f'<div style="display:flex;align-items:center;gap:28px;background:#fff;border-radius:22px;padding:{14 if many else 16}px 26px;font-size:{36 if many else 36}px;width:780px;box-sizing:border-box">{sw}<div>{txt}</div></div>'
        body = f'<div style="display:flex;flex-direction:column;gap:{14 if many else 18}px;margin:auto 0">{rows}</div>'
    return HEAD + title_html(p["a"], p["b"], p["sub"]) + body + FOOT

async def main():
    out = os.path.join(HERE, "pins"); os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page(viewport={"width":1000,"height":1500})
        for p in PINS:
            await pg.set_content(render(p))
            await pg.screenshot(path=os.path.join(out, p["fn"]+".png"), clip={"x":0,"y":0,"width":1000,"height":1500})
        await br.close()
    with open(os.path.join(HERE, "pinterest-bulk.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
        for i,p in enumerate(PINS):
            w.writerow([p["title"][:100], f"{SITE}pins/{p['fn']}.png", p["board"], "", p["desc"][:500], SITE+p["page"],
                        (START+datetime.timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S"), p["kw"]])
    print(len(PINS), "pins")
asyncio.run(main())
