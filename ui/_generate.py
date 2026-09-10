import os, html
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{OUT}/renter", exist_ok=True)
os.makedirs(f"{OUT}/owner", exist_ok=True)
os.makedirs(f"{OUT}/admin", exist_ok=True)
os.makedirs(f"{OUT}/css", exist_ok=True)
os.makedirs(f"{OUT}/js", exist_ok=True)

# ---------------------------------------------------------------- icons
I = {
 "home":'<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
 "search":'<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
 "heart":'<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
 "chat":'<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
 "user":'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 "bell":'<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
 "back":'<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
 "pin":'<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 "calendar":'<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
 "plus":'<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
 "filter":'<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
 "sort":'<line x1="21" y1="10" x2="3" y2="10"/><line x1="21" y1="6" x2="3" y2="6"/><line x1="21" y1="14" x2="3" y2="14"/><line x1="21" y1="18" x2="3" y2="18"/>',
 "map":'<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
 "star":'<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
 "settings":'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
 "logout":'<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
 "check":'<polyline points="20 6 9 17 4 12"/>',
 "x":'<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
 "send":'<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
 "clip":'<path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>',
 "phone":'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "more":'<circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/>',
 "chev":'<polyline points="9 18 15 12 9 6"/>',
 "chevd":'<polyline points="6 9 12 15 18 9"/>',
 "chevl":'<polyline points="15 18 9 12 15 6"/>',
 "eye":'<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
 "mail":'<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
 "lock":'<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "grid":'<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
 "clipboard":'<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>',
 "image":'<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
 "upload":'<polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 4 16.3"/>',
 "share":'<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>',
 "flag":'<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/>',
 "help":'<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
 "bed":'<path d="M3 7v11"/><path d="M3 11h18v7"/><path d="M3 16h18"/><path d="M7 11V9a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v2"/>',
 "bath":'<path d="M4 12h16v2a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M6 12V6a2 2 0 0 1 4 0"/><line x1="7" y1="19" x2="6" y2="21"/><line x1="17" y1="19" x2="18" y2="21"/>',
 "area":'<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>',
 "wifi":'<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>',
 "wind":'<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/>',
 "car":'<path d="M5 17h14l1-6-3-5H7L4 11z"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/>',
 "sofa":'<path d="M4 18v-6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6"/><path d="M2 12v6h20v-6"/><line x1="6" y1="18" x2="6" y2="20"/><line x1="18" y1="18" x2="18" y2="20"/>',
 "users":'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "building":'<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>',
 "alert":'<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
 "edit":'<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>',
 "clock":'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 "shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "camera":'<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
 "trash":'<polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>',
 "ban":'<circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>',
 "menu":'<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>',
 "key":'<path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>',
 "sliders":'<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
}
def ic(name, size=20, cls=""):
    return f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>'

# ---------------------------------------------------------------- data
PH = {
 1:"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=70",
 2:"https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=70",
 3:"https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=70",
 4:"https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&q=70",
 5:"https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&q=70",
 6:"https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=70",
}
ROOMS = [
 dict(id=1,name="Cozy Condo Near BTS",area="Ari, Bangkok",price="10,000",bed=1,bath=1,sqm=30,status="Available",featured=True),
 dict(id=2,name="Modern Studio",area="Phahon Yothin, Bangkok",price="8,500",bed=1,bath=1,sqm=25,status="Reserved"),
 dict(id=3,name="Spacious Apartment",area="Chatuchak, Bangkok",price="12,000",bed=1,bath=1,sqm=20,status="Rented"),
 dict(id=4,name="Condo One Bedroom",area="Sukhumvit, Bangkok",price="15,000",bed=1,bath=1,sqm=35,status="Unavailable"),
 dict(id=5,name="Luxury Room",area="Asoke, Bangkok",price="18,000",bed=1,bath=1,sqm=28,status="Available"),
 dict(id=6,name="Garden House",area="Ladprao, Bangkok",price="15,000",bed=2,bath=1,sqm=48,status="Available"),
]
AV_COLORS = ["#F6D6C8","#CFE3F7","#D8F0DC","#F5E4B8","#E3D6F5","#F7D0DE"]
def avatar(name, size=40, i=0):
    initials="".join(w[0] for w in name.split()[:2]).upper()
    c=AV_COLORS[i%len(AV_COLORS)]
    return f'<span class="avatar" style="width:{size}px;height:{size}px;background:{c};font-size:{int(size*0.36)}px">{initials}</span>'
def photo(n, cls="photo"):
    return f'<img class="{cls}" src="{PH[n]}" alt="" loading="lazy" onerror="this.classList.add(\'fallback\')">'

def badge(text, kind):  # kind: ok warn bad info neutral
    return f'<span class="badge {kind}">{text}</span>'
STATUS_KIND={"Available":"ok","Reserved":"warn","Rented":"bad","Unavailable":"neutral","Pending":"warn","Confirmed":"ok","Completed":"info","Rejected":"bad","Cancelled":"bad","Declined":"bad","Approved":"ok","Published":"ok","Draft":"neutral","Suggested":"info","Requested":"warn","Open":"warn","Reviewed":"info","Actioned":"ok"}
def sbadge(s): return badge(s, STATUS_KIND.get(s,"neutral"))
def dot_status(s): return f'<span class="dotb {STATUS_KIND.get(s,"neutral")}"><i></i>{s}</span>'

# ---------------------------------------------------------------- shells
HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{root}css/style.css">
</head>
<body class="{bodycls}">
'''
FOOT = '''<script src="{root}js/ui.js"></script>
</body>
</html>
'''
def page(path, title, body, bodycls="", root="../"):
    with open(f"{OUT}/{path}","w") as f:
        f.write(HEAD.format(title=title, root=root, bodycls=bodycls)+body+FOOT.format(root=root))

def statusbar(dark=False):
    return f'<div class="statusbar{" light" if dark else ""}"><span>9:41</span><span class="sb-icons"><i class="sig"></i><i class="wifi"></i><i class="bat"></i></span></div>'

RN = [("home","Home","home.html"),("search","Search","search.html"),("heart","Favorites","favorites.html"),("chat","Messages","messages.html"),("user","Profile","profile.html")]
def bottomnav(active):
    items="".join(f'<a href="{h}" class="{"on" if k==active else ""}">{ic(k,22)}<span>{l}</span></a>' for k,l,h in RN)
    return f'<nav class="bottomnav">{items}</nav>'

def phone(content, active=None, dark=False, cls=""):
    nav = bottomnav(active) if active else ""
    return f'''<div class="canvas"><div class="phone {cls}">{statusbar(dark)}<div class="screen">{content}</div>{nav}</div></div>'''

def topbar(title, right="", back="javascript:history.back()"):
    return f'<header class="topbar"><a class="iconbtn" href="{back}">{ic("back",22)}</a><h1>{title}</h1><span class="right">{right}</span></header>'

# ---------------------------------------------------------------- renter pages
def room_card(r, i, wide=False, fav=False):
    heart = f'<button class="heart {"on" if fav else ""}" data-fav>{ic("heart",18)}</button>'
    feat = '<span class="feat">Featured</span>' if r.get("featured") and wide else ""
    return f'''<a class="roomcard {"wide" if wide else ""}" href="room.html">
  <div class="thumb">{photo(r["id"])}{feat}{heart}</div>
  <div class="rc-body">
    <div class="rc-name">{r["name"]}</div>
    <div class="rc-area">{r["area"]}</div>
    <div class="rc-price"><b>฿{r["price"]}</b> / month</div>
    <div class="rc-meta"><span>{ic("bed",15)} {r["bed"]}</span><span>{ic("bath",15)} {r["bath"]}</span><span>{ic("area",15)} {r["sqm"]} m²</span></div>
  </div></a>'''

def room_row(r, right="", href="room.html", sub=None):
    sub = sub if sub is not None else f'<div class="rc-area">{r["area"]}</div><div class="rc-price"><b>฿{r["price"]}</b> / month</div>'
    return f'''<a class="roomrow" href="{href}"><div class="thumb sm">{photo(r["id"])}</div>
  <div class="rr-body"><div class="rc-name">{r["name"]}</div>{sub}</div><span class="rr-right">{right}</span></a>'''

# 1 welcome
page("renter/welcome.html","RoomStay",phone(f'''
<div class="hero-img">{photo(5,"cover")}<div class="hero-fade"></div>
  <div class="hero-brand"><span class="logo lg">{ic("home",26)}</span><h1>RoomStay</h1><p>Find your perfect room<br>Live a better tomorrow</p></div>
</div>
<div class="hero-actions">
  <a class="btn primary block" href="signup.html">Get Started</a>
  <a class="btn outline block" href="login.html">Log In</a>
  <p class="fine">A trusted room rental platform for students and professionals</p>
</div>''', dark=True, cls="hero"))

# 2 signup
page("renter/signup.html","Create account",phone(f'''
{topbar("", back="welcome.html")}
<div class="pad">
  <h1 class="h1">Create Your Account</h1><p class="sub">Join RoomStay and find your new home</p>
  <label class="field"><span>Full Name</span><div class="input">{ic("user",18)}<input value="Su Yi Nandar"></div></label>
  <label class="field"><span>Email</span><div class="input">{ic("mail",18)}<input value="suyi@example.com"></div></label>
  <label class="field"><span>Password</span><div class="input">{ic("lock",18)}<input type="password" value="password123">{ic("eye",18)}</div></label>
  <label class="field"><span>I want to</span><div class="seg"><button class="on">Rent a room</button><button>List my property</button></div></label>
  <label class="check"><input type="checkbox" checked><span>I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a></span></label>
  <a class="btn primary block" href="home.html">Sign Up</a>
  <p class="fine center">Already have an account? <a href="login.html">Log in</a></p>
</div>'''))

# 3 login
page("renter/login.html","Log in",phone(f'''
{topbar("", back="welcome.html")}
<div class="pad">
  <div class="logo-row"><span class="logo">{ic("home",22)}</span><div><b>RoomStay</b><small>Find. Rent. Belong.</small></div></div>
  <h1 class="h1">Welcome back</h1><p class="sub">Log in to continue</p>
  <label class="field"><span>Email</span><div class="input">{ic("mail",18)}<input value="suyi@example.com"></div></label>
  <label class="field"><span>Password</span><div class="input">{ic("lock",18)}<input type="password" value="password123">{ic("eye",18)}</div></label>
  <p class="fine right"><a href="#">Forgot password?</a></p>
  <a class="btn primary block" href="home.html">Log In</a>
  <p class="fine center">New here? <a href="signup.html">Create an account</a></p>
  <div class="divider"><span>Demo accounts</span></div>
  <div class="demo-links"><a class="btn ghost" href="home.html">Renter</a><a class="btn ghost" href="../owner/dashboard.html">Owner</a><a class="btn ghost" href="../admin/dashboard.html">Admin</a></div>
</div>'''))

# 4 home
cats="".join(f'<a class="cat" href="search.html"><span class="cat-ic">{ic(k,20)}</span>{l}</a>' for k,l in [("building","Apartments"),("grid","Condos"),("home","Houses"),("bed","Rooms")])
page("renter/home.html","Home",phone(f'''
<header class="apphead">
  <div class="logo-row"><span class="logo">{ic("home",22)}</span><div><b>RoomStay</b><small>Find. Rent. Belong.</small></div></div>
  <a class="iconbtn" href="notifications.html">{ic("bell",22)}<i class="pip"></i></a>
</header>
<div class="pad">
  <a class="searchbox" href="search.html">{ic("search",18)}<span>Search by location, university, or keyword</span></a>
  <div class="cats">{cats}</div>
  <div class="promo"><div><b>A place to call home</b><p>Comfortable rooms for a brighter you</p></div>{photo(6)}</div>
  <div class="sec-head"><h2>Featured Rooms</h2><a href="search.html">See all</a></div>
  {room_card(ROOMS[0],0,wide=True,fav=True)}
  {room_card(ROOMS[1],1,wide=True)}
  <div class="sec-head"><h2>Near you</h2><a href="search.html">See all</a></div>
  {room_row(ROOMS[4])}
  {room_row(ROOMS[5])}
</div>''', active="home"))

# 5 search results
page("renter/search.html","Search",phone(f'''
<div class="pad top">
  <div class="searchbox live">{ic("search",18)}<input value="Ari, Bangkok"><button class="clear">{ic("x",14)}</button></div>
  <div class="chips-row">
    <a class="chip" href="filters.html">{ic("sliders",15)} Filter</a>
    <button class="chip">{ic("sort",15)} Sort {ic("chevd",13)}</button>
    <button class="chip">{ic("map",15)} Map</button>
  </div>
  <p class="count">128 rooms found</p>
  {room_card(ROOMS[0],0,wide=True,fav=True)}
  {room_card(ROOMS[1],1,wide=True)}
  {room_card(ROOMS[2],2,wide=True)}
  {room_row(ROOMS[3])}
  {room_row(ROOMS[4])}
</div>''', active="search"))

# 6 filters
fac="".join(f'<label class="check"><input type="checkbox" {"checked" if c else ""}><span>{n}</span></label>' for n,c in [("Wi-Fi",1),("Air Conditioner",1),("Furnished",0),("Parking",0),("Elevator",0),("Security",0)])
page("renter/filters.html","Filters",phone(f'''
{topbar("Filters", right='<a class="link" href="#">Reset</a>', back="search.html")}
<div class="pad">
  <label class="field"><span>Location</span><div class="input select"><input value="Ari, Bangkok">{ic("chevd",18)}</div></label>
  <div class="field"><span>Price Range (per month)</span>
    <div class="range"><div class="track"><div class="fill" style="left:22%;right:38%"></div><i style="left:22%"></i><i style="right:38%"></i></div><div class="range-lbl"><span>฿3,000</span><span>฿50,000</span></div></div></div>
  <div class="field"><span>Room Type</span><div class="pills"><button class="pill on">All</button><button class="pill">Apartment</button><button class="pill">Condo</button><button class="pill">House</button><button class="pill">Room</button></div></div>
  <div class="field"><span>Bedrooms</span><div class="pills"><button class="pill on">Any</button><button class="pill">1</button><button class="pill">2</button><button class="pill">3+</button></div></div>
  <div class="field"><span>Facilities</span><div class="checklist">{fac}</div></div>
  <div class="field"><span>Availability</span><div class="pills"><button class="pill on">Available now</button><button class="pill">From a date</button></div></div>
</div>
<div class="sticky-cta"><a class="btn primary block" href="search.html">Show 128 Results</a></div>'''))

# 7 room detail
tags="".join(f'<span class="tag">{t}</span>' for t in ["Fully Furnished","BTS 5 min","Pet Friendly","Wi-Fi","Air Conditioner"])
page("renter/room.html","Cozy Condo Near BTS",phone(f'''
<div class="gallery">{photo(1,"cover")}
  <a class="iconbtn glass tl" href="javascript:history.back()">{ic("back",20)}</a>
  <span class="tr"><button class="iconbtn glass on" data-fav>{ic("heart",18)}</button><button class="iconbtn glass">{ic("share",18)}</button></span>
  <span class="counter">1/10</span>
</div>
<div class="pad">
  <div class="title-row"><h1 class="h1">Cozy Condo Near BTS</h1>{dot_status("Available")}</div>
  <div class="price-lg"><b>฿10,000</b> / month</div>
  <div class="rc-area">{ic("pin",14)} Ari, Bangkok</div>
  <div class="rc-meta lg"><span>{ic("bed",16)} 1 Bed</span><span>{ic("bath",16)} 1 Bath</span><span>{ic("area",16)} 30 m²</span></div>
  <div class="tags">{tags}</div>
  <h2 class="h2">Description</h2>
  <p class="body">A cozy and comfortable condo near BTS Ari. Fully furnished with bed, wardrobe, desk, air conditioner, and free Wi-Fi. Suitable for students and working professionals. <a href="#">Read more</a></p>
  <h2 class="h2">Location</h2>
  <div class="map-box"><div class="map-grid"></div><span class="map-pin">{ic("pin",22)}</span><span class="map-lbl">Ari, Phaya Thai, Bangkok</span></div>
  <h2 class="h2">About the Owner</h2>
  <div class="owner-row">{avatar("Thana K",44,1)}<div><b>Mr. Thana</b><small>Member since 2022 · {ic("star",12)} 4.8 (32 reviews)</small></div><a class="btn ghost sm" href="#">View Profile</a></div>
  <h2 class="h2">Reviews <small class="muted">(32)</small></h2>
  <div class="review">{avatar("Alice Johnson",36,0)}<div><div class="rv-head"><b>Alice Johnson</b><span class="stars">★★★★★</span></div><p>Clean room, kind owner, very close to BTS. Highly recommend.</p><small>2 weeks ago</small></div></div>
  <div class="review">{avatar("Michael Brown",36,2)}<div><div class="rv-head"><b>Michael Brown</b><span class="stars">★★★★☆</span></div><p>Good value. Wi-Fi is fast. Slightly noisy on weekends.</p><small>1 month ago</small></div></div>
  <a class="report" href="#">{ic("flag",14)} Report this listing</a>
</div>
<div class="sticky-cta two"><a class="btn outline" href="chat.html">Message</a><a class="btn primary" href="request-viewing.html">Request Viewing</a></div>'''))

# 8 chat
page("renter/chat.html","Chat",phone(f'''
<header class="topbar chat-head"><a class="iconbtn" href="messages.html">{ic("back",22)}</a>{avatar("Thana K",36,1)}<div class="who"><b>Mr. Thana</b><small class="online">Online</small></div><span class="right"><button class="iconbtn">{ic("phone",20)}</button><button class="iconbtn">{ic("more",20)}</button></span></header>
<div class="pad chat">
  <div class="ctx-card">{photo(1)}<div><b>Cozy Condo Near BTS</b><small>Ari, Bangkok · ฿10,000 / month</small></div></div>
  <div class="day">Today</div>
  <div class="msg me">Hi! Is the room still available?<time>10:05 AM</time></div>
  <div class="msg them">Yes, it is still available. When would you like to see it?<time>10:07 AM</time></div>
  <div class="msg me">Can I visit this weekend?<time>10:08 AM</time></div>
  <div class="msg them">Sure! How about Saturday at 2 PM?<time>10:10 AM</time></div>
  <div class="msg me">That works for me. See you then!<time>10:11 AM</time></div>
</div>
<div class="composer"><button class="iconbtn">{ic("clip",20)}</button><input placeholder="Type a message..."><button class="sendbtn">{ic("send",18)}</button></div>'''))

# 8b messages list
convos=[("Thana K","Mr. Thana","Sure! How about Saturday at 2 PM?","10:10 AM",1,1),("Somchai P","Somchai P.","The room will be free from June 1.","Yesterday",0,3),("Nattaporn K","Nattaporn K.","Thank you for your interest!","Mon",0,5),("Kanya S","Kanya S.","Yes, parking is included.","12 May",0,4)]
rows="".join(f'<a class="convo" href="chat.html">{avatar(a,46,i)}<div class="cv-body"><div class="cv-top"><b>{n}</b><time>{t}</time></div><p>{m}</p></div>{"<span class=\'count-pip\'>"+str(u)+"</span>" if u else ""}</a>' for a,n,m,t,u,i in convos)
page("renter/messages.html","Messages",phone(f'''
<div class="pad top"><h1 class="h1">Messages</h1>
  <div class="searchbox live">{ic("search",18)}<input placeholder="Search conversations"></div>
  <div class="list">{rows}</div></div>''', active="chat"))

# 9 request viewing
days="".join(f'<button class="{ "on" if d==14 else ""}{" dim" if d in (25,26,27,28,29,30,31) and n<7 else ""}">{d}</button>' for n,d in enumerate([25,26,27,28,29,30,31,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5]))
page("renter/request-viewing.html","Request viewing",phone(f'''
{topbar("Request Viewing", back="room.html")}
<div class="pad">
  <div class="ctx-card">{photo(1)}<div><b>Cozy Condo Near BTS</b><small>Ari, Bangkok</small><small><b>฿10,000</b> / month</small></div></div>
  <div class="field"><span>Select Date</span>
    <div class="cal"><div class="cal-head"><button class="iconbtn">{ic("chevl",18)}</button><b>June 2025</b><button class="iconbtn">{ic("chev",18)}</button></div>
      <div class="cal-dow"><span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span></div>
      <div class="cal-grid">{days}</div></div></div>
  <div class="field"><span>Select Time</span><div class="pills wrap"><button class="pill">10:00 AM</button><button class="pill on">02:00 PM</button><button class="pill">04:00 PM</button><button class="pill">06:00 PM</button></div></div>
  <label class="field"><span>Message (Optional)</span><textarea rows="3">I would like to see the room and know more details.</textarea></label>
  <div class="note info">{ic("clock",16)} The owner can approve, suggest another time, or decline with a reason. You will get a notification.</div>
</div>
<div class="sticky-cta"><a class="btn primary block" href="bookings.html">Send Request</a></div>'''))

# 10 favorites
page("renter/favorites.html","Favorites",phone(f'''
<div class="pad top"><h1 class="h1">My Favorites</h1>
  {room_row(ROOMS[0], right=f'<button class="heart on flat" data-fav>{ic("heart",18)}</button>')}
  {room_row(ROOMS[1], right=f'<button class="heart on flat" data-fav>{ic("heart",18)}</button>')}
  {room_row(ROOMS[2], right=f'<button class="heart on flat" data-fav>{ic("heart",18)}</button>')}
  {room_row(ROOMS[5], right=f'<button class="heart on flat" data-fav>{ic("heart",18)}</button>')}
</div>''', active="heart"))

# 11 bookings
def bk_row(r, status, sub, href="booking-details.html"):
    return room_row(r, right=sbadge(status), href=href, sub=f'<div class="rc-area">{r["area"]}</div><div class="rc-price"><b>฿{r["price"]}</b> / month</div><small class="muted">{sub}</small>')
page("renter/bookings.html","My Bookings",phone(f'''
<div class="pad top"><div class="title-row"><h1 class="h1">My Bookings</h1><button class="iconbtn">{ic("search",20)}</button></div>
  <div class="tabs"><a class="on" href="#">All</a><a href="#">Pending <i class="tab-pip">1</i></a><a href="#">Viewings</a><a href="#">Completed</a></div>
  <h3 class="h3">Active</h3>
  {bk_row(ROOMS[0],"Pending","Requested 18 May 2025 · waiting for owner")}
  {bk_row(ROOMS[1],"Confirmed","Move in: 1 Jun 2025")}
  <h3 class="h3">Viewing requests</h3>
  {room_row(ROOMS[4], right=sbadge("Suggested"), href="booking-details.html", sub='<div class="rc-area">Asoke, Bangkok</div><small class="muted">Owner suggested Sun 15 Jun, 11:00 AM</small><div class="mini-actions"><button class="btn primary xs">Accept time</button><button class="btn ghost xs">Re-request</button></div>')}
  <h3 class="h3">Past bookings</h3>
  {bk_row(ROOMS[2],"Completed","1 May 2024 to 30 Apr 2025", href="review.html")}
  {bk_row(ROOMS[3],"Cancelled","Cancelled on 10 Apr 2025")}
</div>''', active="user"))

# 12 booking details
steps=[("Booking Request","10 Jun 2025, 14:20","done"),("Approved by Owner","11 Jun 2025, 09:15","done"),("Booking Confirmed","Room marked as Rented","done"),("Move in","1 Jul 2025","next"),("Completed","Leave a review after the rental","")]
tl="".join(f'<div class="step {s}"><i>{n+1}</i><div><b>{t}</b><small>{d}</small></div></div>' for n,(t,d,s) in enumerate(steps))
page("renter/booking-details.html","Booking details",phone(f'''
{topbar("Booking Details", back="bookings.html")}
<div class="pad">
  <div class="ctx-card">{photo(2)}<div><b>Modern Studio</b><small>Phahon Yothin, Bangkok</small><small><b>฿8,500</b> / month</small></div>{sbadge("Confirmed")}</div>
  <div class="tabs"><a class="on" href="#">Overview</a><a href="chat.html">Messages</a><a href="#">History</a></div>
  <dl class="kv">
    <dt>Booking ID</dt><dd>BK-2025-0614-001</dd>
    <dt>Owner</dt><dd>{avatar("Thana K",22,1)} Mr. Thana</dd>
    <dt>Move-in Date</dt><dd>1 Jul 2025</dd>
    <dt>Rental period</dt><dd>12 months</dd>
    <dt>Monthly rent</dt><dd>฿8,500</dd>
    <dt>Status</dt><dd>{sbadge("Confirmed")}</dd>
  </dl>
  <h2 class="h2">Progress</h2>
  <div class="timeline">{tl}</div>
  <div class="note ok">{ic("check",16)} Your booking is confirmed. Contact the owner in Messages to arrange the move-in.</div>
  <button class="btn outline block danger-text">Cancel Booking</button>
</div>'''))

# 13 review
page("renter/review.html","Leave a review",phone(f'''
{topbar("Leave a Review", back="bookings.html")}
<div class="pad">
  <div class="ctx-card">{photo(3)}<div><b>Spacious Apartment</b><small>Chatuchak, Bangkok</small><small>Stayed 1 May 2024 to 30 Apr 2025</small></div></div>
  <div class="field"><span>Your Rating</span><div class="star-input"><b class="on">★</b><b class="on">★</b><b class="on">★</b><b class="on">★</b><b class="on">★</b></div></div>
  <label class="field"><span>Your Review</span><textarea rows="4">The room is clean and comfortable. The owner is very kind and responsive. Highly recommend!</textarea></label>
  <div class="field"><span>Add photos (optional)</span><div class="photo-row"><div class="thumb sm">{photo(3)}</div><div class="thumb sm">{photo(4)}</div><button class="thumb sm add">{ic("plus",22)}</button></div></div>
  <div class="note info">{ic("shield",16)} Only renters with a completed booking can review. Reviews are public on the listing.</div>
</div>
<div class="sticky-cta"><a class="btn primary block" href="bookings.html">Submit Review</a></div>'''))

# 14 profile
menu=[("clipboard","My Bookings","bookings.html"),("heart","My Favorites","favorites.html"),("chat","My Messages","messages.html"),("bell","Notifications","notifications.html"),("settings","Settings","#"),("help","Help & Support","#")]
mrows="".join(f'<a class="menu-row" href="{h}"><span class="mi">{ic(k,18)}</span>{l}{ic("chev",18,"chev")}</a>' for k,l,h in menu)
page("renter/profile.html","Profile",phone(f'''
<div class="pad top">
  <div class="prof-head">{avatar("Su Yi Nandar",56,0)}<div><b>Su Yi Nandar</b><small>suyi@example.com</small><small class="muted">Renter</small></div><button class="iconbtn">{ic("edit",18)}</button></div>
  <div class="menu">{mrows}</div>
  <a class="partner-card" href="../owner/dashboard.html"><span class="mi">{ic("building",18)}</span><div><b>Become a Partner</b><small>List your property and reach renters</small></div>{ic("chev",18,"chev")}</a>
  <a class="menu-row danger" href="welcome.html"><span class="mi">{ic("logout",18)}</span>Log out</a>
</div>''', active="user"))

# 15 notifications
notes=[("check","ok","Booking confirmed","Mr. Thana accepted your booking for Modern Studio.","10:15 AM"),("calendar","warn","New time suggested","Owner suggested Sun 15 Jun, 11:00 AM for Luxury Room viewing.","Yesterday"),("chat","info","New message","Mr. Thana: Sure! How about Saturday at 2 PM?","Yesterday"),("x","bad","Viewing declined","Owner declined viewing for Garden House: room already reserved.","12 May")]
nrows="".join(f'<div class="note-row"><span class="mi {k}">{ic(i,16)}</span><div><b>{t}</b><p>{b}</p><small>{d}</small></div></div>' for i,k,t,b,d in notes)
page("renter/notifications.html","Notifications",phone(f'''
{topbar("Notifications", right='<a class="link" href="#">Mark all as read</a>', back="home.html")}
<div class="pad"><h3 class="h3">Today</h3>{nrows}</div>''', active="home"))

# ---------------------------------------------------------------- owner (desktop)
ON=[("grid","Dashboard","dashboard.html",""),("building","My Listings","listings.html",""),("clipboard","Booking Requests","booking-requests.html","3"),("calendar","Viewing Requests","viewing-requests.html","1"),("chat","Messages","messages.html","5"),("star","Reviews","reviews.html",""),("user","Profile","profile.html",""),("settings","Settings","#","")]
def sidebar(active, brand=("RoomStay","Owner Partner"), items=None, root="../"):
    items=items or ON
    lis="".join(f'<a href="{h}" class="{"on" if l==active else ""}">{ic(k,18)}<span>{l}</span>{f"<i class=\'pip-n {"warn" if l.startswith("Viewing") else ""}\'>{n}</i>" if n else ""}</a>' for k,l,h,n in items)
    return f'''<aside class="side"><div class="logo-row"><span class="logo">{ic("home",22)}</span><div><b>{brand[0]}</b><small>{brand[1]}</small></div></div>
    <nav class="sidenav">{lis}</nav><a class="sidenav-out" href="{root}renter/welcome.html">{ic("logout",18)}<span>Logout</span></a></aside>'''
def desk(active, main, brand=("RoomStay","Owner Partner"), items=None, root="../"):
    return f'<div class="desk">{sidebar(active,brand,items,root)}<main class="main">{main}</main></div>'
def deskhead(title, sub="", who=("Su Yi Nandar","Partner Owner"), right=""):
    return f'''<header class="deskhead"><div><small class="muted">{sub}</small><h1>{title}</h1></div>
    <div class="dh-right">{right}<a class="iconbtn" href="#">{ic("bell",20)}<i class="pip"></i></a><div class="me">{avatar(who[0],36,0)}<div><b>{who[0]}</b><small>{who[1]}</small></div>{ic("chevd",16)}</div></div></header>'''

def stat(icon, color, label, value, sub):
    return f'<div class="stat"><span class="stat-ic" style="background:{color}">{ic(icon,18)}</span><div><small>{label}</small><b>{value}</b><span>{sub}</span></div></div>'

# dashboard
req_rows=[("Alice Johnson",0,ROOMS[0],"18 May 2025","Pending","Accept","Reject"),("Michael Brown",2,ROOMS[1],"17 May 2025","Confirmed","View","Message"),("Sophia Lee",3,ROOMS[2],"16 May 2025","Requested","Approve","Suggest time")]
trs="".join(f'<tr><td><span class="cell-user">{avatar(n,28,i)}{n}</span></td><td><span class="cell-room">{photo(r["id"])}{r["name"]}</span></td><td>{d}</td><td>{sbadge(s)}</td><td class="actions"><a class="btn primary xs" href="booking-details.html">{a}</a><a class="btn ghost xs" href="#">{b}</a></td></tr>' for n,i,r,d,s,a,b in req_rows)
page("owner/dashboard.html","Owner Dashboard",desk("Dashboard",f'''
{deskhead("Welcome back, Su Yi Nandar","Manage your properties, bookings and viewings.", right=f'<span class="datebox">{ic("calendar",16)}<div><small>Today</small><b>18 May 2025</b></div></span>')}
<div class="stats">
  {stat("home","#5B4FE9","Total Listings","5","4 Published")}
  {stat("clock","#E39B0E","Pending Requests","3","Awaiting your reply")}
  {stat("calendar","#3B82F6","Bookings","12","This month")}
  {stat("star","#22A06B","Average Rating","4.8","From 32 reviews")}
</div>
<div class="grid-2 wide-left">
  <section class="card"><div class="card-head"><h2>Recent Requests</h2><a class="link" href="booking-requests.html">View all</a></div>
    <table class="tbl"><thead><tr><th>Renter</th><th>Property</th><th>Request date</th><th>Status</th><th>Action</th></tr></thead><tbody>{trs}</tbody></table></section>
  <section class="card"><div class="card-head"><h2>Rooms Overview</h2></div>
    <div class="occ"><div class="occ-row"><span>{dot_status("Available")}</span><b>2</b></div><div class="occ-row"><span>{dot_status("Reserved")}</span><b>1</b></div><div class="occ-row"><span>{dot_status("Rented")}</span><b>1</b></div><div class="occ-row"><span>{dot_status("Unavailable")}</span><b>1</b></div></div>
    <div class="bar-stack"><i style="width:40%;background:#22A06B"></i><i style="width:20%;background:#E39B0E"></i><i style="width:20%;background:#E0453B"></i><i style="width:20%;background:#B8BDCC"></i></div>
  </section>
</div>
<div class="grid-2 wide-left">
  <section class="card"><div class="card-head"><h2>Quick Actions</h2></div>
    <div class="quick"><a href="add-property.html"><span class="mi">{ic("plus",20)}</span>Add New Listing</a><a href="booking-requests.html"><span class="mi">{ic("clipboard",20)}</span>Booking Requests</a><a href="viewing-requests.html"><span class="mi">{ic("calendar",20)}</span>Viewing Requests</a><a href="messages.html"><span class="mi">{ic("chat",20)}</span>Messages</a></div></section>
  <section class="card"><div class="card-head"><h2>Bookings Overview</h2></div>
    <div class="big-num">12 <span class="delta">↑ 20%</span></div><small class="muted">from last month</small>
    <svg class="spark" viewBox="0 0 260 70" preserveAspectRatio="none"><path d="M0 55 L30 48 L60 52 L90 40 L120 44 L150 30 L180 34 L210 20 L240 24 L260 10" fill="none" stroke="#5B4FE9" stroke-width="2.5" stroke-linejoin="round"/><path d="M0 55 L30 48 L60 52 L90 40 L120 44 L150 30 L180 34 L210 20 L240 24 L260 10 V70 H0z" fill="#5B4FE9" opacity=".08"/></svg>
  </section>
</div>'''))

# listings
lrows=""
for i,r in enumerate(ROOMS[:5]):
    pub = "Published" if r["status"]!="Unavailable" else "Draft"
    lrows+=f'''<div class="listing"><div class="thumb">{photo(r["id"])}</div>
    <div class="l-body"><b>{r["name"]}</b><small>{r["area"]}</small><div class="rc-price"><b>฿{r["price"]}</b> / month</div>
      <div class="rc-meta"><span>{ic("bed",15)} {r["bed"]}</span><span>{ic("bath",15)} {r["bath"]}</span><span>{ic("area",15)} {r["sqm"]} m²</span></div><small class="muted">{[245,312,198,0,176][i]} views · {[12,18,9,0,7][i]} inquiries</small></div>
    <div class="l-status">{sbadge(pub)}{dot_status(r["status"])}</div>
    <div class="l-actions"><a class="btn ghost sm" href="add-property.html">Edit</a><button class="iconbtn">{ic("more",18)}</button></div></div>'''
page("owner/listings.html","My Listings",desk("My Listings",f'''
{deskhead("My Listings","5 properties", right=f'<a class="btn primary" href="add-property.html">{ic("plus",16)} Add New Listing</a>')}
<div class="card">
  <div class="tabs"><a class="on" href="#">All (5)</a><a href="#">Published (4)</a><a href="#">Draft (1)</a><a href="#">Reserved (1)</a><a href="#">Rented (1)</a></div>
  <div class="listings">{lrows}</div></div>'''))

# add property
facs="".join(f'<label class="fac {"on" if o else ""}"><input type="checkbox" {"checked" if o else ""}>{ic(k,20)}<span>{l}</span></label>' for k,l,o in [("wifi","Wi-Fi",1),("wind","Air Conditioner",1),("sofa","Furnished",1),("car","Parking",0),("building","Elevator",1),("shield","Security",0)])
page("owner/add-property.html","Add New Property",desk("My Listings",f'''
{deskhead("Add New Property","My Listings / New")}
<div class="card form-card">
  <div class="stepper"><div class="st on"><i>1</i><span>Basic Information</span></div><div class="st"><i>2</i><span>Details &amp; Photos</span></div><div class="st"><i>3</i><span>Review &amp; Publish</span></div></div>
  <div class="grid-2">
    <div>
      <h2 class="h2">Basic Information</h2>
      <label class="field"><span>Property Title <em>*</em></span><div class="input"><input value="Modern Studio"></div></label>
      <label class="field"><span>Property Type <em>*</em></span><div class="input select"><input value="Condo">{ic("chevd",18)}</div></label>
      <label class="field"><span>Location <em>*</em></span><div class="input">{ic("pin",18)}<input value="Phahon Yothin, Bangkok"></div></label>
      <label class="field"><span>Address <em>*</em></span><div class="input"><input value="123 Phahon Yothin Rd, Chatuchak, Bangkok 10900"></div></label>
      <div class="grid-2"><label class="field"><span>Monthly Rent (฿) <em>*</em></span><div class="input"><input value="8,500"></div></label>
      <label class="field"><span>Available From <em>*</em></span><div class="input">{ic("calendar",18)}<input value="June 1, 2025"></div></label></div>
      <div class="grid-3"><label class="field"><span>Bedrooms</span><div class="input"><input value="1"></div></label><label class="field"><span>Bathrooms</span><div class="input"><input value="1"></div></label><label class="field"><span>Size (m²)</span><div class="input"><input value="25"></div></label></div>
      <label class="field"><span>Description <em>*</em></span><textarea rows="4">Modern and cozy studio near BTS. Fully furnished with bed, wardrobe, desk, air conditioner and free Wi-Fi. Suitable for students and working professionals.</textarea></label>
    </div>
    <div>
      <h2 class="h2">Facilities</h2><div class="facs">{facs}</div>
      <h2 class="h2">Photos</h2>
      <div class="photo-row"><div class="thumb">{photo(2)}</div><div class="thumb">{photo(4)}</div><button class="thumb add">{ic("upload",22)}<span>Add More</span></button></div>
      <h2 class="h2">Availability Status</h2>
      <div class="pills"><button class="pill on">Available</button><button class="pill">Reserved</button><button class="pill">Rented</button><button class="pill">Unavailable</button></div>
    </div>
  </div>
  <div class="form-foot"><a class="btn ghost" href="listings.html">Save as Draft</a><a class="btn primary" href="listings.html">Next {ic("chev",16)}</a></div>
</div>'''))

# booking requests
brs=[("Alice Johnson",0,ROOMS[0],"18 May 2025","1 Jun 2025","Pending"),("Michael Brown",2,ROOMS[1],"17 May 2025","1 Jun 2025","Confirmed"),("Nattaporn K",4,ROOMS[2],"15 May 2025","15 Jun 2025","Confirmed"),("John Smith",5,ROOMS[5],"12 May 2025","1 Jun 2025","Rejected"),("Emily Wong",1,ROOMS[0],"10 May 2025","20 May 2025","Cancelled")]
def br_actions(s):
    if s=="Pending": return f'<a class="btn primary xs" href="booking-details.html">Accept</a><a class="btn ghost xs danger-text" href="#">Reject</a>'
    return f'<a class="btn ghost xs" href="booking-details.html">View</a><a class="btn ghost xs" href="messages.html">Message</a>'
btr="".join(f'<tr><td><span class="cell-user">{avatar(n,28,i)}{n}</span></td><td><span class="cell-room">{photo(r["id"])}{r["name"]}</span></td><td>{d}</td><td>{m}</td><td>{sbadge(s)}</td><td class="actions">{br_actions(s)}</td></tr>' for n,i,r,d,m,s in brs)
page("owner/booking-requests.html","Booking Requests",desk("Booking Requests",f'''
{deskhead("Booking Requests","3 waiting for your decision")}
<div class="card"><div class="tabs"><a class="on" href="#">All</a><a href="#">Pending <i class="tab-pip">1</i></a><a href="#">Confirmed</a><a href="#">History</a></div>
<table class="tbl"><thead><tr><th>Renter</th><th>Property</th><th>Requested</th><th>Move-in</th><th>Status</th><th>Action</th></tr></thead><tbody>{btr}</tbody></table></div>'''))

# viewing requests
vrs=[("Su Yi Nandar",0,ROOMS[1],"Sat 15 Jun 2025, 10:00 AM","Requested"),("Alex Chen",1,ROOMS[0],"Sat 15 Jun 2025, 02:00 PM","Approved"),("Nattaporn K",4,ROOMS[2],"Sun 16 Jun 2025, 11:00 AM","Suggested"),("Maya R",3,ROOMS[4],"Mon 17 Jun 2025, 03:00 PM","Declined")]
def vr_card(n,i,r,t,s):
    if s=="Requested": act=f'<button class="btn primary sm">{ic("check",14)} Approve</button><button class="btn ghost sm">{ic("clock",14)} Suggest another time</button><button class="btn ghost sm danger-text">{ic("x",14)} Decline</button>'
    elif s=="Suggested": act='<small class="muted">You suggested Sun 16 Jun, 11:00 AM. Waiting for the renter to agree.</small>'
    elif s=="Declined": act='<small class="muted">Reason sent: room is being repainted that week.</small>'
    else: act='<a class="btn ghost sm" href="messages.html">Message renter</a>'
    return f'<div class="vr"><div class="vr-top">{avatar(n,40,i)}<div><b>{n}</b><small>{r["name"]} · {r["area"]}</small></div>{sbadge(s)}</div><div class="vr-time">{ic("calendar",16)} {t}</div><div class="vr-act">{act}</div></div>'
page("owner/viewing-requests.html","Viewing Requests",desk("Viewing Requests",f'''
{deskhead("Viewing Requests","1 new request")}
<div class="card"><div class="tabs"><a class="on" href="#">All</a><a href="#">New <i class="tab-pip warn">1</i></a><a href="#">Upcoming</a><a href="#">Completed</a></div>
<div class="vr-list">{"".join(vr_card(*v) for v in vrs)}</div></div>'''))

# booking details (owner)
page("owner/booking-details.html","Booking Details",desk("Booking Requests",f'''
{deskhead("Booking Details","Booking Requests / BK-2025-0518-001")}
<div class="grid-2 wide-left">
  <section class="card">
    <div class="ctx-card lg">{photo(1)}<div><b>Cozy Condo Near BTS</b><small>Ari, Bangkok</small><small><b>฿10,000</b> / month</small></div>{sbadge("Pending")}</div>
    <div class="tabs"><a class="on" href="#">Overview</a><a href="messages.html">Messages</a><a href="#">History</a></div>
    <dl class="kv two">
      <dt>Booking ID</dt><dd>BK-2025-0518-001</dd>
      <dt>Renter</dt><dd>{avatar("Alice Johnson",22,0)} Alice Johnson <small class="muted">alice@email.com</small></dd>
      <dt>Requested on</dt><dd>18 May 2025, 14:20</dd>
      <dt>Move-in Date</dt><dd>1 Jun 2025</dd>
      <dt>Rental period</dt><dd>12 months</dd>
      <dt>Monthly rent</dt><dd>฿10,000</dd>
      <dt>Viewing</dt><dd>Completed on Sat 10 May, 2:00 PM</dd>
      <dt>Renter note</dt><dd>I work near Ari and would like to move in at the start of June.</dd>
    </dl>
    <div class="note warn">{ic("clock",16)} Accepting this booking will mark the room as Rented and reject other pending requests for it.</div>
    <div class="form-foot start"><button class="btn primary">{ic("check",16)} Accept Booking</button><button class="btn outline danger-text">{ic("x",16)} Reject</button><a class="btn ghost" href="messages.html">Message renter</a></div>
  </section>
  <section class="card"><div class="card-head"><h2>Timeline</h2></div>
    <div class="timeline">
      <div class="step done"><i>1</i><div><b>Viewing requested</b><small>5 May 2025</small></div></div>
      <div class="step done"><i>2</i><div><b>Viewing completed</b><small>10 May 2025, 2:00 PM</small></div></div>
      <div class="step done"><i>3</i><div><b>Booking request</b><small>18 May 2025, 14:20</small></div></div>
      <div class="step next"><i>4</i><div><b>Your decision</b><small>Accept or reject</small></div></div>
      <div class="step"><i>5</i><div><b>Confirmed</b><small>Room becomes Rented</small></div></div>
    </div>
    <div class="card-head"><h2>About the renter</h2></div>
    <div class="owner-row">{avatar("Alice Johnson",44,0)}<div><b>Alice Johnson</b><small>Member since 2024 · 2 completed rentals</small></div></div>
  </section>
</div>'''))

# messages (owner)
oconv=[("Alice Johnson","Thank you! I will visit t...","10:30 AM",2,0),("Michael Brown","Is the room still available?","09:15 AM",0,2),("Sophia Lee","Can I see more photos?","Yesterday",0,3),("David Kim","I would like to book this room.","17 May",0,5),("Emily Wong","What is the nearest BTS station?","16 May",0,1)]
ocv="".join(f'<a class="convo {"on" if n==0 else ""}" href="#">{avatar(a,44,i)}<div class="cv-body"><div class="cv-top"><b>{a}</b><time>{t}</time></div><p>{m}</p></div>{"<span class=\'count-pip\'>"+str(u)+"</span>" if u else ""}</a>' for n,(a,m,t,u,i) in enumerate(oconv))
page("owner/messages.html","Messages",desk("Messages",f'''
{deskhead("Messages","5 unread")}
<div class="card msg-layout">
  <div class="msg-list"><div class="searchbox live">{ic("search",18)}<input placeholder="Search conversations"></div>{ocv}</div>
  <div class="msg-pane">
    <header class="chat-head">{avatar("Alice Johnson",40,0)}<div class="who"><b>Alice Johnson</b><small class="online">Online</small></div><span class="right"><button class="iconbtn">{ic("phone",20)}</button><button class="iconbtn">{ic("more",20)}</button></span></header>
    <div class="chat">
      <div class="ctx-card">{photo(1)}<div><b>Cozy Condo Near BTS</b><small>Ari, Bangkok · ฿10,000 / month</small></div></div>
      <div class="msg them">Hi! Is the room still available?<time>10:05 AM</time></div>
      <div class="msg me">Yes, it is still available. When would you like to see it?<time>10:07 AM</time></div>
      <div class="msg them">Can I visit this weekend?<time>10:08 AM</time></div>
      <div class="msg me">Sure! How about Saturday at 2 PM?<time>10:10 AM</time></div>
      <div class="msg them">That works for me. See you then!<time>10:11 AM</time></div>
    </div>
    <div class="composer"><button class="iconbtn">{ic("clip",20)}</button><input placeholder="Type a message..."><button class="sendbtn">{ic("send",18)}</button></div>
  </div>
</div>'''))

# reviews (owner)
rv=[("Alice Johnson",0,ROOMS[0],5,"Clean room, kind owner, very close to BTS. Highly recommend.","2 weeks ago"),("Michael Brown",2,ROOMS[1],4,"Good value. Wi-Fi is fast. Slightly noisy on weekends.","1 month ago"),("Nattaporn K",4,ROOMS[2],5,"Owner responded quickly and the move-in was smooth.","2 months ago")]
rvs="".join(f'<div class="review card-row">{avatar(n,40,i)}<div><div class="rv-head"><b>{n}</b><span class="stars">{"★"*s}{"☆"*(5-s)}</span></div><small class="muted">{r["name"]}</small><p>{t}</p><small>{d}</small></div><a class="btn ghost xs" href="#">{ic("flag",13)} Report</a></div>' for n,i,r,s,t,d in rv)
page("owner/reviews.html","Reviews",desk("Reviews",f'''
{deskhead("Reviews","32 reviews across 5 listings")}
<div class="stats three">{stat("star","#22A06B","Average rating","4.8","From 32 reviews")}{stat("users","#5B4FE9","Reviewers","32","Completed rentals only")}{stat("clock","#E39B0E","This month","3","New reviews")}</div>
<div class="card">{rvs}</div>'''))

# profile (owner)
prow="".join(f'<a class="menu-row" href="#"><span class="mi">{ic(k,18)}</span>{l}<small class="muted">{s}</small>{ic("chev",18,"chev")}</a>' for k,l,s in [("user","Personal Information",""),("building","Business Information",""),("image","Documents","3 files uploaded"),("bell","Notification Settings",""),("lock","Change Password","")])
page("owner/profile.html","Profile",desk("Profile",f'''
{deskhead("Profile","Account")}
<div class="grid-2">
  <section class="card center-col">{avatar("Su Yi Nandar",96,0)}<b class="name">Su Yi Nandar</b><small>suyi@example.com</small><span class="badge info">{ic("shield",12)} Verified Partner</span>
    <dl class="kv"><dt>Member since</dt><dd>March 2022</dd><dt>Listings</dt><dd>5</dd><dt>Rating</dt><dd>4.8 / 5</dd></dl></section>
  <section class="card"><div class="menu">{prow}</div></section>
</div>'''))

# ---------------------------------------------------------------- admin
AN=[("grid","Dashboard","dashboard.html",""),("users","Users","users.html",""),("building","Listings","listings.html",""),("flag","Reports","reports.html","4"),("star","Reviews","#",""),("clipboard","Bookings","#",""),("settings","Settings","#","")]
adm=("RoomStay","Admin")
def adesk(active, main): return desk(active, main, brand=adm, items=AN)
utr="".join(f'<tr><td><span class="cell-user">{avatar(n,28,i)}{n}</span></td><td>{e}</td><td>{badge(r,"info" if r=="Owner" else "neutral")}</td><td>{d}</td><td>{sbadge(s)}</td><td class="actions"><a class="btn ghost xs" href="#">View</a><a class="btn ghost xs danger-text" href="#">{"Disable" if s!="Suspended" else "Enable"}</a></td></tr>' for n,i,e,r,d,s in [("Su Yi Nandar",0,"suyi@example.com","Renter","12 Jan 2025","Active"),("Thana K",1,"thana@example.com","Owner","3 Mar 2022","Active"),("Alice Johnson",2,"alice@email.com","Renter","8 Feb 2025","Active"),("Peter Tan",5,"peter@email.com","Owner","20 Apr 2025","Suspended")])
STATUS_KIND.update({"Active":"ok","Suspended":"bad","Resolved":"ok"})
rtr="".join(f'<tr><td>{badge(t,"neutral")}</td><td>{x}</td><td>{r}</td><td><span class="cell-user">{avatar(n,24,i)}{n}</span></td><td>{d}</td><td>{sbadge(s)}</td><td class="actions"><a class="btn ghost xs" href="#">Review</a></td></tr>' for t,x,r,n,i,d,s in [("Listing","Garden House","Photos do not match the room","Emily Wong",1,"17 May 2025","Open"),("User","Peter Tan","Asked for payment before viewing","Alice Johnson",2,"16 May 2025","Open"),("Listing","Condo One Bedroom","Listing is outdated","David Kim",5,"14 May 2025","Reviewed"),("Review","Modern Studio","Offensive language","Thana K",1,"10 May 2025","Actioned")])
page("admin/dashboard.html","Admin Dashboard",adesk("Dashboard",f'''
{deskhead("Admin Dashboard","Platform overview", who=("Admin User","Administrator"))}
<div class="stats">{stat("users","#5B4FE9","Users","1,248","+36 this week")}{stat("building","#3B82F6","Listings","412","387 published")}{stat("clipboard","#22A06B","Bookings","96","This month")}{stat("flag","#E0453B","Open Reports","4","Need review")}</div>
<div class="card"><div class="card-head"><h2>Open Reports</h2><a class="link" href="reports.html">View all</a></div>
<table class="tbl"><thead><tr><th>Type</th><th>Target</th><th>Reason</th><th>Reported by</th><th>Date</th><th>Status</th><th></th></tr></thead><tbody>{rtr}</tbody></table></div>
<div class="card"><div class="card-head"><h2>Recent Users</h2><a class="link" href="users.html">View all</a></div>
<table class="tbl"><thead><tr><th>User</th><th>Email</th><th>Role</th><th>Joined</th><th>Status</th><th>Action</th></tr></thead><tbody>{utr}</tbody></table></div>'''))
page("admin/users.html","Users",adesk("Users",f'''{deskhead("Users","1,248 accounts", who=("Admin User","Administrator"), right=f'<div class="searchbox live sm">{ic("search",16)}<input placeholder="Search users"></div>')}
<div class="card"><div class="tabs"><a class="on" href="#">All</a><a href="#">Renters</a><a href="#">Owners</a><a href="#">Suspended</a></div>
<table class="tbl"><thead><tr><th>User</th><th>Email</th><th>Role</th><th>Joined</th><th>Status</th><th>Action</th></tr></thead><tbody>{utr}</tbody></table></div>'''))
page("admin/reports.html","Reports",adesk("Reports",f'''{deskhead("Reports","4 open", who=("Admin User","Administrator"))}
<div class="card"><div class="tabs"><a class="on" href="#">Open</a><a href="#">Reviewed</a><a href="#">Actioned</a></div>
<table class="tbl"><thead><tr><th>Type</th><th>Target</th><th>Reason</th><th>Reported by</th><th>Date</th><th>Status</th><th></th></tr></thead><tbody>{rtr}</tbody></table></div>'''))
altr="".join(f'<tr><td><span class="cell-room">{photo(r["id"])}{r["name"]}</span></td><td>Thana K</td><td>฿{r["price"]}</td><td>{dot_status(r["status"])}</td><td>{sbadge("Published" if r["status"]!="Unavailable" else "Draft")}</td><td class="actions"><a class="btn ghost xs" href="#">View</a><a class="btn ghost xs danger-text" href="#">Disable</a></td></tr>' for r in ROOMS)
page("admin/listings.html","Listings",adesk("Listings",f'''{deskhead("Listings","412 listings", who=("Admin User","Administrator"))}
<div class="card"><table class="tbl"><thead><tr><th>Property</th><th>Owner</th><th>Rent</th><th>Room status</th><th>Listing</th><th>Action</th></tr></thead><tbody>{altr}</tbody></table></div>'''))

# ---------------------------------------------------------------- index board
R_SCREENS=[("welcome","Welcome"),("signup","Create account"),("login","Log in"),("home","Home"),("search","Search results"),("filters","Filters"),("room","Room detail"),("chat","Chat"),("request-viewing","Request viewing"),("favorites","Favorites"),("bookings","My bookings"),("booking-details","Booking details"),("review","Leave a review"),("profile","Profile"),("messages","Messages"),("notifications","Notifications")]
O_SCREENS=[("dashboard","Dashboard"),("listings","My listings"),("add-property","Add property"),("booking-requests","Booking requests"),("viewing-requests","Viewing requests"),("booking-details","Booking details"),("messages","Messages"),("reviews","Reviews"),("profile","Profile")]
A_SCREENS=[("dashboard","Dashboard"),("users","Users"),("listings","Listings"),("reports","Reports")]
def frames(folder, screens, kind):
    return "".join(f'<a class="frame {kind}" href="{folder}/{f}.html" target="_blank"><div class="frame-view"><iframe src="{folder}/{f}.html" loading="lazy" tabindex="-1"></iframe></div><span>{l}</span></a>' for f,l in screens)
page("index.html","RoomStay UI",f'''
<div class="board">
  <header class="board-head"><div class="logo-row"><span class="logo">{ic("home",22)}</span><div><b>RoomStay</b><small>Condo &amp; Apartment Rental System</small></div></div>
    <p>UI design, static HTML and CSS, no backend. Click any screen to open it full size.</p></header>
  <h2 class="board-title">Renter UI <small>mobile</small></h2>
  <div class="frames">{frames("renter",R_SCREENS,"m")}</div>
  <h2 class="board-title">Owner UI <small>desktop</small></h2>
  <div class="frames">{frames("owner",O_SCREENS,"d")}</div>
  <h2 class="board-title">Admin UI <small>desktop</small></h2>
  <div class="frames">{frames("admin",A_SCREENS,"d")}</div>
</div>''', bodycls="board-body", root="")

# ---------------------------------------------------------------- JS
open(f"{OUT}/js/ui.js","w").write('''// Small interactions only. No data, no backend.
document.addEventListener('click', function (e) {
  var fav = e.target.closest('[data-fav]');
  if (fav) { e.preventDefault(); fav.classList.toggle('on'); return; }
  var pill = e.target.closest('.pill');
  if (pill && pill.parentElement.classList.contains('pills')) {
    pill.parentElement.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('on'); });
    pill.classList.add('on'); e.preventDefault(); return;
  }
  var tab = e.target.closest('.tabs > a');
  if (tab && tab.getAttribute('href') === '#') {
    tab.parentElement.querySelectorAll('a').forEach(function (t) { t.classList.remove('on'); });
    tab.classList.add('on'); e.preventDefault(); return;
  }
  var star = e.target.closest('.star-input b');
  if (star) {
    var all = Array.prototype.slice.call(star.parentElement.children), idx = all.indexOf(star);
    all.forEach(function (s, i) { s.classList.toggle('on', i <= idx); });
  }
  var seg = e.target.closest('.seg button');
  if (seg) { seg.parentElement.querySelectorAll('button').forEach(function (b) { b.classList.remove('on'); }); seg.classList.add('on'); e.preventDefault(); }
  var day = e.target.closest('.cal-grid button');
  if (day && !day.classList.contains('dim')) { day.parentElement.querySelectorAll('button').forEach(function (b) { b.classList.remove('on'); }); day.classList.add('on'); }
});
''')
print("pages written")
