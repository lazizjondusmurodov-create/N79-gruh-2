import { useState, useEffect } from "react";

const hashPassword = async (password) => {
  const encoder = new TextEncoder();
  const data = encoder.encode(password + "auth_salt_2025");
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
};

const generateToken = () =>
  Math.random().toString(36).slice(2) + Date.now().toString(36);

const DB = {
  async getUsers() {
    try {
      const r = await window.storage.get("auth:users");
      return r ? JSON.parse(r.value) : {};
    } catch { return {}; }
  },
  async saveUsers(users) {
    await window.storage.set("auth:users", JSON.stringify(users));
  },
  async getSession() {
    try {
      const r = await window.storage.get("auth:session");
      return r ? JSON.parse(r.value) : null;
    } catch { return null; }
  },
  async saveSession(session) {
    await window.storage.set("auth:session", JSON.stringify(session));
  },
  async clearSession() {
    try { await window.storage.delete("auth:session"); } catch {}
  },
};

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
  *{box-sizing:border-box;margin:0;padding:0}
  :root{
    --bg:#0a0a0f;
    --surface:#13131c;
    --surface2:#1c1c2a;
    --border:#2a2a3d;
    --accent:#7c6af7;
    --accent2:#a78bfa;
    --text:#f0effe;
    --muted:#6b6b8a;
    --success:#34d399;
    --danger:#f87171;
    --font-head:'Syne',sans-serif;
    --font-body:'DM Sans',sans-serif;
  }
  body{background:var(--bg);color:var(--text);font-family:var(--font-body)}
  .app{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:1rem;position:relative;overflow:hidden}
  .grid-bg{position:fixed;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:40px 40px;opacity:0.3;pointer-events:none}
  .glow{position:fixed;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(124,106,247,0.12) 0%,transparent 70%);top:-200px;left:-200px;pointer-events:none}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:2.5rem;width:100%;max-width:440px;position:relative;z-index:1}
  .logo{font-family:var(--font-head);font-size:22px;font-weight:800;color:var(--accent2);letter-spacing:-0.5px;margin-bottom:2rem;display:flex;align-items:center;gap:8px}
  .logo-dot{width:8px;height:8px;background:var(--accent);border-radius:50%;margin-top:2px}
  h1{font-family:var(--font-head);font-size:28px;font-weight:700;line-height:1.2;margin-bottom:6px;letter-spacing:-0.5px}
  .subtitle{color:var(--muted);font-size:14px;margin-bottom:2rem;font-weight:300}
  label{display:block;font-size:12px;font-weight:500;color:var(--muted);letter-spacing:0.5px;text-transform:uppercase;margin-bottom:6px}
  .field{margin-bottom:1.25rem}
  input{width:100%;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:12px 14px;color:var(--text);font-family:var(--font-body);font-size:15px;outline:none;transition:border-color .2s,box-shadow .2s}
  input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,106,247,.15)}
  input::placeholder{color:var(--muted)}
  .btn{width:100%;padding:13px;border-radius:8px;font-family:var(--font-head);font-size:15px;font-weight:600;cursor:pointer;border:none;transition:all .2s;margin-top:.5rem}
  .btn-primary{background:var(--accent);color:#fff}
  .btn-primary:hover{background:#6b5ae0;transform:translateY(-1px)}
  .btn-primary:active{transform:translateY(0)}
  .btn-primary:disabled{opacity:.5;cursor:not-allowed;transform:none}
  .divider{display:flex;align-items:center;gap:12px;margin:1.5rem 0;color:var(--muted);font-size:13px}
  .divider::before,.divider::after{content:'';flex:1;height:1px;background:var(--border)}
  .link-btn{background:none;border:none;color:var(--accent2);cursor:pointer;font-size:14px;font-family:var(--font-body);text-decoration:underline;padding:0}
  .link-btn:hover{color:var(--text)}
  .alert{padding:12px 14px;border-radius:8px;font-size:13px;margin-bottom:1rem;display:flex;align-items:center;gap:8px}
  .alert-error{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:var(--danger)}
  .alert-success{background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);color:var(--success)}
  .dash{min-height:100vh;background:var(--bg);font-family:var(--font-body)}
  .dash-nav{background:var(--surface);border-bottom:1px solid var(--border);padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between}
  .nav-logo{font-family:var(--font-head);font-size:18px;font-weight:800;color:var(--accent2);display:flex;align-items:center;gap:8px}
  .nav-user{display:flex;align-items:center;gap:12px}
  .avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-family:var(--font-head);font-size:14px;font-weight:700;color:#fff}
  .btn-logout{background:var(--surface2);border:1px solid var(--border);color:var(--muted);padding:8px 16px;border-radius:8px;font-family:var(--font-body);font-size:13px;cursor:pointer;transition:all .2s}
  .btn-logout:hover{border-color:var(--danger);color:var(--danger)}
  .dash-body{padding:3rem 2rem;max-width:900px;margin:0 auto}
  .welcome-box{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:2rem;margin-bottom:2rem}
  .welcome-box h2{font-family:var(--font-head);font-size:26px;font-weight:700;margin-bottom:6px}
  .welcome-box p{color:var(--muted);font-size:14px;font-weight:300}
  .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem}
  .stat-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.25rem}
  .stat-label{font-size:11px;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.5rem}
  .stat-value{font-family:var(--font-head);font-size:22px;font-weight:700;color:var(--accent2)}
  .tag{display:inline-block;background:rgba(124,106,247,.15);color:var(--accent2);border-radius:6px;padding:3px 10px;font-size:12px;font-weight:500}
  .spinner{width:16px;height:16px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:spin .6s linear infinite;display:inline-block;vertical-align:middle;margin-right:6px}
  @keyframes spin{to{transform:rotate(360deg)}}
  .fade{animation:fadeIn .35s ease}
  @keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
`;

function Alert({ type, msg }) {
  if (!msg) return null;
  return <div className={`alert alert-${type}`}>{msg}</div>;
}

function LoginForm({ onSwitch, onLogin }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handle = async () => {
    setError("");
    if (!form.email || !form.password) return setError("Barcha maydonlarni to'ldiring.");
    setLoading(true);
    try {
      const users = await DB.getUsers();
      const user = users[form.email.toLowerCase()];
      if (!user) { setError("Bu email bilan foydalanuvchi topilmadi."); setLoading(false); return; }
      const hash = await hashPassword(form.password);
      if (hash !== user.password) { setError("Parol noto'g'ri."); setLoading(false); return; }
      const session = { userId: user.id, email: user.email, name: user.name, loginAt: new Date().toISOString(), token: generateToken() };
      await DB.saveSession(session);
      onLogin(session);
    } catch { setError("Xatolik yuz berdi. Qayta urinib ko'ring."); }
    setLoading(false);
  };

  return (
    <div className="card fade">
      <div className="logo"><div className="logo-dot" />Vault</div>
      <h1>Xush kelibsiz</h1>
      <p className="subtitle">Davom etish uchun hisobingizga kiring</p>
      <Alert type="error" msg={error} />
      <div className="field">
        <label>Email manzil</label>
        <input type="email" placeholder="siz@misol.uz" value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))} />
      </div>
      <div className="field">
        <label>Parol</label>
        <input type="password" placeholder="••••••••" value={form.password} onChange={e => setForm(p => ({ ...p, password: e.target.value }))} onKeyDown={e => e.key === "Enter" && handle()} />
      </div>
      <button className="btn btn-primary" onClick={handle} disabled={loading}>
        {loading && <span className="spinner" />}{loading ? "Tekshirilmoqda..." : "Kirish"}
      </button>
      <div className="divider">yoki</div>
      <p style={{ textAlign: "center", fontSize: 14, color: "var(--muted)" }}>
        Hisobingiz yo'qmi?{" "}
        <button className="link-btn" onClick={onSwitch}>Ro'yxatdan o'ting</button>
      </p>
    </div>
  );
}

function RegisterForm({ onSwitch, onLogin }) {
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handle = async () => {
    setError("");
    if (!form.name || !form.email || !form.password || !form.confirm) return setError("Barcha maydonlarni to'ldiring.");
    if (form.password.length < 6) return setError("Parol kamida 6 belgidan iborat bo'lishi kerak.");
    if (form.password !== form.confirm) return setError("Parollar mos kelmayapti.");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) return setError("Email manzil noto'g'ri.");
    setLoading(true);
    try {
      const users = await DB.getUsers();
      if (users[form.email.toLowerCase()]) { setError("Bu email allaqachon ro'yxatdan o'tgan."); setLoading(false); return; }
      const hash = await hashPassword(form.password);
      const user = { id: generateToken(), name: form.name.trim(), email: form.email.toLowerCase(), password: hash, createdAt: new Date().toISOString() };
      users[form.email.toLowerCase()] = user;
      await DB.saveUsers(users);
      const session = { userId: user.id, email: user.email, name: user.name, loginAt: new Date().toISOString(), token: generateToken() };
      await DB.saveSession(session);
      onLogin(session);
    } catch { setError("Xatolik yuz berdi. Qayta urinib ko'ring."); }
    setLoading(false);
  };

  return (
    <div className="card fade">
      <div className="logo"><div className="logo-dot" />Vault</div>
      <h1>Hisob yarating</h1>
      <p className="subtitle">Bir necha soniyada ro'yxatdan o'ting</p>
      <Alert type="error" msg={error} />
      <div className="field">
        <label>To'liq ism</label>
        <input type="text" placeholder="Alisher Navoiy" value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
      </div>
      <div className="field">
        <label>Email manzil</label>
        <input type="email" placeholder="siz@misol.uz" value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))} />
      </div>
      <div className="field">
        <label>Parol</label>
        <input type="password" placeholder="Kamida 6 belgi" value={form.password} onChange={e => setForm(p => ({ ...p, password: e.target.value }))} />
      </div>
      <div className="field">
        <label>Parolni tasdiqlang</label>
        <input type="password" placeholder="••••••••" value={form.confirm} onChange={e => setForm(p => ({ ...p, confirm: e.target.value }))} onKeyDown={e => e.key === "Enter" && handle()} />
      </div>
      <button className="btn btn-primary" onClick={handle} disabled={loading}>
        {loading && <span className="spinner" />}{loading ? "Yaratilmoqda..." : "Hisob yaratish"}
      </button>
      <div className="divider">yoki</div>
      <p style={{ textAlign: "center", fontSize: 14, color: "var(--muted)" }}>
        Hisobingiz bormi?{" "}
        <button className="link-btn" onClick={onSwitch}>Kiring</button>
      </p>
    </div>
  );
}

function Dashboard({ session, onLogout }) {
  const [userCount, setUserCount] = useState("...");
  const loginTime = new Date(session.loginAt);
  const initials = session.name.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase();

  useEffect(() => {
    DB.getUsers().then(u => setUserCount(Object.keys(u).length));
  }, []);

  const handleLogout = async () => {
    await DB.clearSession();
    onLogout();
  };

  return (
    <div className="dash fade">
      <style>{styles}</style>
      <nav className="dash-nav">
        <div className="nav-logo"><div className="logo-dot" />Vault</div>
        <div className="nav-user">
          <div className="avatar">{initials}</div>
          <span style={{ fontSize: 14, color: "var(--muted)" }}>{session.name}</span>
          <button className="btn-logout" onClick={handleLogout}>Chiqish</button>
        </div>
      </nav>
      <div className="dash-body">
        <div className="welcome-box">
          <h2>Xush kelibsiz, {session.name.split(" ")[0]}! 👋</h2>
          <p>Hisob muvaffaqiyatli autentifikatsiya qilindi. Siz xavfsiz kirdingiz.</p>
        </div>
        <div className="stats">
          <div className="stat-card">
            <div className="stat-label">Holat</div>
            <div className="stat-value" style={{ color: "var(--success)", fontSize: 16 }}>● Aktiv</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Kirish vaqti</div>
            <div className="stat-value" style={{ fontSize: 14 }}>{loginTime.toLocaleTimeString("uz-UZ")}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Jami foydalanuvchi</div>
            <div className="stat-value">{userCount}</div>
          </div>
        </div>
        <div className="stat-card" style={{ padding: "1.5rem" }}>
          <div className="stat-label" style={{ marginBottom: "1rem" }}>Sessiya ma'lumotlari</div>
          {[
            ["Foydalanuvchi ID", session.userId.slice(0, 16) + "..."],
            ["Email", session.email],
            ["Token", session.token.slice(0, 20) + "..."],
          ].map(([k, v]) => (
            <div key={k} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: "1px solid var(--border)" }}>
              <span style={{ color: "var(--muted)", fontSize: 13 }}>{k}</span>
              <span className="tag">{v}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("login");
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    DB.getSession().then(s => { setSession(s); setLoading(false); });
  }, []);

  if (loading) return (
    <>
      <style>{styles}</style>
      <div className="app"><div className="grid-bg" /><div className="glow" /><div className="spinner" style={{ width: 32, height: 32, borderWidth: 3 }} /></div>
    </>
  );

  if (session) return (
    <>
      <style>{styles}</style>
      <Dashboard session={session} onLogout={() => setSession(null)} />
    </>
  );

  return (
    <>
      <style>{styles}</style>
      <div className="app">
        <div className="grid-bg" />
        <div className="glow" />
        {page === "login"
          ? <LoginForm onSwitch={() => setPage("register")} onLogin={setSession} />
          : <RegisterForm onSwitch={() => setPage("login")} onLogin={setSession} />}
      </div>
    </>
  );
}
