import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Meta RC Pulse | 宇宙型ランディングページ",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit default chrome cleanup
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML = r"""
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Meta RC Pulse</title>
  <style>
    :root{
      --bg:#030712;
      --panel:rgba(5,10,24,.62);
      --panel2:rgba(255,255,255,.055);
      --line:rgba(255,255,255,.14);
      --emerald:#5fffd2;
      --cyan:#54d8ff;
      --blue:#337dff;
      --white:#fff;
      --muted:#a9b7c7;
      --danger:#ff6b6b;
      --gold:#f8d37a;
    }

    *{box-sizing:border-box;}
    html,body{
      margin:0;
      padding:0;
      width:100%;
      min-height:100%;
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;
      background:var(--bg);
      color:var(--white);
      overflow:hidden;
    }

    body{
      background:
        radial-gradient(circle at 50% 115%, rgba(49,132,255,.22), transparent 30%),
        radial-gradient(circle at 78% 12%, rgba(84,216,255,.15), transparent 26%),
        radial-gradient(circle at 18% 20%, rgba(95,255,210,.10), transparent 30%),
        linear-gradient(180deg,#02040b 0%,#06101f 48%,#02040b 100%);
    }

    .space-bg{
      position:fixed;
      inset:0;
      z-index:-3;
      overflow:hidden;
      background: radial-gradient(ellipse at bottom, rgba(31,82,145,.20), transparent 42%);
    }
    .stars, .stars2, .stars3{
      position:absolute;
      inset:-20%;
      background-repeat:repeat;
      opacity:.85;
      transform:rotate(-8deg);
    }
    .stars{
      background-image:
        radial-gradient(circle, rgba(255,255,255,.9) 0 1px, transparent 1.5px),
        radial-gradient(circle, rgba(84,216,255,.8) 0 1px, transparent 1.5px);
      background-size:90px 90px, 150px 150px;
      animation: drift 72s linear infinite;
      filter:blur(.1px);
    }
    .stars2{
      background-image:radial-gradient(circle, rgba(255,255,255,.62) 0 1px, transparent 1.7px);
      background-size:220px 220px;
      animation: drift2 115s linear infinite;
      opacity:.55;
    }
    .stars3{
      background-image:radial-gradient(circle, rgba(255,255,255,.38) 0 1px, transparent 1.8px);
      background-size:330px 330px;
      animation: drift3 160s linear infinite;
      opacity:.42;
    }
    .earth-glow{
      position:absolute;
      left:50%;
      bottom:-28vh;
      transform:translateX(-50%);
      width:150vw;
      height:48vh;
      border-radius:50% 50% 0 0;
      background:radial-gradient(ellipse at center, rgba(69,154,255,.34), rgba(65,255,219,.08) 42%, transparent 70%);
      filter:blur(18px);
      opacity:.72;
    }
    @keyframes drift{ from{transform:translate3d(0,0,0) rotate(-8deg);} to{transform:translate3d(-260px,360px,0) rotate(-8deg);} }
    @keyframes drift2{ from{transform:translate3d(0,0,0) rotate(-8deg);} to{transform:translate3d(240px,460px,0) rotate(-8deg);} }
    @keyframes drift3{ from{transform:translate3d(0,0,0) rotate(-8deg);} to{transform:translate3d(-180px,520px,0) rotate(-8deg);} }

    .app{
      height:100vh;
      width:100vw;
      overflow-y:scroll;
      scroll-snap-type:y mandatory;
      scroll-behavior:smooth;
    }
    .slide{
      min-height:100vh;
      width:100%;
      scroll-snap-align:start;
      position:relative;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:92px 18px 72px;
    }
    .inner{
      width:min(1120px,100%);
      margin:0 auto;
      text-align:center;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
    }
    .nav{
      position:fixed;
      top:16px;
      left:16px;
      right:16px;
      z-index:50;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      pointer-events:none;
    }
    .brand,.nav-actions{
      pointer-events:auto;
      display:flex;
      align-items:center;
      gap:10px;
      border:1px solid var(--line);
      background:rgba(0,0,0,.36);
      backdrop-filter:blur(18px);
      border-radius:999px;
      padding:9px 12px;
      box-shadow:0 0 34px rgba(84,216,255,.08);
    }
    .logo{
      width:34px;height:34px;border-radius:50%;
      background:linear-gradient(135deg,var(--emerald),var(--cyan));
      display:grid;place-items:center;
      color:#00111d;font-weight:900;
    }
    .brand-text{line-height:1.1;text-align:left;}
    .brand-text strong{font-size:14px;display:block;}
    .brand-text span{font-size:10px;color:var(--muted);letter-spacing:.18em;text-transform:uppercase;}
    .nav a{
      text-decoration:none;
      color:white;
      font-size:13px;
      font-weight:700;
      padding:8px 12px;
      border-radius:999px;
    }
    .nav a.primary{background:white;color:#03101a;}
    .nav a.ghost{border:1px solid rgba(255,255,255,.12);}

    .voice-btn{
      position:fixed;
      top:82px;
      right:18px;
      z-index:60;
      border:1px solid rgba(84,216,255,.36);
      background:rgba(0,0,0,.44);
      color:#eaffff;
      border-radius:999px;
      padding:11px 14px;
      display:flex;gap:8px;align-items:center;
      font-weight:800;
      box-shadow:0 0 28px rgba(84,216,255,.16);
      backdrop-filter:blur(16px);
      cursor:pointer;
    }
    .voice-btn:hover{background:rgba(84,216,255,.12);}
    .voice-panel{
      position:fixed;
      top:132px;
      right:18px;
      width:min(360px,calc(100vw - 36px));
      z-index:65;
      border:1px solid rgba(84,216,255,.28);
      background:rgba(3,8,20,.86);
      backdrop-filter:blur(22px);
      border-radius:24px;
      padding:20px;
      box-shadow:0 26px 80px rgba(0,0,0,.45),0 0 45px rgba(84,216,255,.13);
      display:none;
      text-align:left;
    }
    .voice-panel.open{display:block;}
    .voice-panel h3{margin:0 0 8px;font-size:18px;}
    .voice-panel p{margin:0 0 16px;color:var(--muted);font-size:13px;line-height:1.8;}
    .voice-panel button{
      width:100%;
      border:1px solid rgba(255,255,255,.14);
      background:rgba(255,255,255,.07);
      color:white;
      border-radius:14px;
      padding:12px;
      margin-top:8px;
      font-weight:800;
      cursor:pointer;
    }
    .voice-panel button.primary{background:linear-gradient(135deg,var(--emerald),var(--cyan));color:#00131d;border:0;}
    .voice-panel button:hover{filter:brightness(1.08);}

    .pill{
      display:inline-flex;
      align-items:center;
      gap:8px;
      border:1px solid rgba(95,255,210,.28);
      background:rgba(95,255,210,.09);
      color:#c8fff3;
      border-radius:999px;
      padding:7px 13px;
      font-size:12px;
      font-weight:800;
      letter-spacing:.02em;
    }
    .kicker{
      color:var(--emerald);
      letter-spacing:.32em;
      text-transform:uppercase;
      font-size:12px;
      font-weight:900;
      margin-bottom:18px;
    }
    h1,h2,h3,p{max-width:100%;}
    h1{
      margin:0;
      font-size:clamp(45px,9.6vw,96px);
      line-height:1.02;
      letter-spacing:-.06em;
      font-weight:1000;
      text-wrap:balance;
    }
    h2{
      margin:0;
      font-size:clamp(34px,6.4vw,68px);
      line-height:1.05;
      letter-spacing:-.045em;
      font-weight:1000;
      text-wrap:balance;
    }
    .grad{
      background:linear-gradient(90deg,#fff,var(--emerald),var(--cyan),#fff);
      -webkit-background-clip:text;background-clip:text;color:transparent;
      filter:drop-shadow(0 0 24px rgba(84,216,255,.16));
    }
    .lead{
      margin:24px auto 0;
      max-width:780px;
      color:#cbd6e4;
      font-size:clamp(15px,2.6vw,19px);
      line-height:2;
      text-wrap:pretty;
    }
    .actions{
      margin-top:34px;
      display:flex;
      justify-content:center;
      align-items:center;
      gap:14px;
      flex-wrap:wrap;
    }
    .btn{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      min-height:50px;
      padding:14px 22px;
      border-radius:999px;
      text-decoration:none;
      color:white;
      font-weight:900;
      border:1px solid rgba(255,255,255,.15);
      background:rgba(255,255,255,.07);
      box-shadow:0 12px 50px rgba(0,0,0,.24);
    }
    .btn.primary{background:linear-gradient(135deg,var(--emerald),var(--cyan),var(--blue));color:#00131d;border:0;box-shadow:0 0 40px rgba(84,216,255,.20);}
    .grid{display:grid;gap:18px;width:100%;margin-top:34px;}
    .grid.two{grid-template-columns:repeat(2,minmax(0,1fr));}
    .grid.three{grid-template-columns:repeat(3,minmax(0,1fr));}
    .grid.four{grid-template-columns:repeat(4,minmax(0,1fr));}
    .card{
      border:1px solid var(--line);
      background:linear-gradient(180deg,rgba(255,255,255,.075),rgba(255,255,255,.035));
      backdrop-filter:blur(20px);
      border-radius:28px;
      padding:24px;
      box-shadow:0 24px 70px rgba(0,0,0,.28);
      text-align:left;
    }
    .card.center{text-align:center;}
    .card h3{margin:0 0 10px;font-size:19px;}
    .card p,.card li{color:#b9c6d8;line-height:1.75;font-size:14px;}
    .card ul{margin:14px 0 0;padding-left:0;list-style:none;}
    .card li{margin:8px 0;display:flex;gap:8px;}
    .card li::before{content:'✓';color:var(--emerald);font-weight:900;}
    .price{
      font-size:clamp(42px,7vw,68px);
      line-height:1;
      font-weight:1000;
      margin:16px 0;
      color:var(--emerald);
      letter-spacing:-.06em;
    }
    .price small{font-size:16px;color:#bcc7d6;letter-spacing:0;}
    .flow{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:32px;}
    .flow-item{
      border:1px solid rgba(95,255,210,.22);
      background:rgba(95,255,210,.08);
      border-radius:22px;
      padding:15px 18px;
      min-width:136px;
      font-weight:900;
      color:#eaffff;
    }
    .arrow{color:var(--cyan);font-size:22px;font-weight:900;}
    .form{
      width:min(520px,100%);
      margin:30px auto 0;
      padding:24px;
      border:1px solid rgba(84,216,255,.24);
      background:rgba(3,8,20,.68);
      backdrop-filter:blur(22px);
      border-radius:28px;
      box-shadow:0 0 55px rgba(84,216,255,.10);
      text-align:left;
    }
    .form label{display:block;font-size:13px;color:#d7e8f5;margin:0 0 8px;font-weight:800;}
    .form input{
      width:100%;
      border:1px solid rgba(255,255,255,.14);
      background:rgba(255,255,255,.07);
      color:white;
      border-radius:15px;
      padding:14px 14px;
      margin-bottom:16px;
      outline:none;
      font-size:15px;
    }
    .form input:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(84,216,255,.12);}
    .note{font-size:12px;color:#8492a5;line-height:1.8;margin-top:14px;}
    .scroll-indicator{
      position:absolute;
      bottom:20px;
      left:50%;
      transform:translateX(-50%);
      font-size:11px;
      color:#94a3b8;
      letter-spacing:.14em;
      text-align:center;
      opacity:.72;
    }
    .scroll-indicator span{display:block;font-size:18px;margin-top:5px;animation:bounce 1.8s infinite;}
    @keyframes bounce{50%{transform:translateY(5px);}}

    .switcher{
      position:fixed;
      left:50%;bottom:16px;
      transform:translateX(-50%);
      display:flex;gap:8px;
      z-index:55;
      background:rgba(0,0,0,.28);
      border:1px solid rgba(255,255,255,.12);
      backdrop-filter:blur(16px);
      padding:7px;
      border-radius:999px;
    }
    .dot{
      width:8px;height:8px;border-radius:50%;
      background:rgba(255,255,255,.32);
    }

    @media (max-width: 820px){
      html,body{overflow:hidden;}
      .slide{padding:92px 16px 74px;}
      .nav{left:10px;right:10px;top:10px;}
      .nav-actions a.ghost{display:none;}
      .brand{padding:8px 10px;}
      .brand-text span{display:none;}
      .voice-btn{top:70px;right:10px;padding:9px 11px;font-size:12px;}
      .voice-panel{top:112px;right:10px;width:calc(100vw - 20px);}
      .grid.two,.grid.three,.grid.four{grid-template-columns:1fr;}
      .grid{gap:12px;margin-top:24px;}
      .card{padding:18px;border-radius:22px;}
      .actions{gap:10px;margin-top:26px;}
      .btn{width:100%;min-height:50px;padding:13px 18px;}
      .flow{gap:8px;}
      .flow-item{min-width:100%;}
      .arrow{transform:rotate(90deg);}
      .form{padding:18px;border-radius:22px;}
      .switcher{display:none;}
      .kicker{font-size:10px;letter-spacing:.24em;}
      .lead{line-height:1.85;}
    }
  </style>
</head>
<body>
  <div class="space-bg">
    <div class="stars"></div>
    <div class="stars2"></div>
    <div class="stars3"></div>
    <div class="earth-glow"></div>
  </div>

  <nav class="nav">
    <div class="brand">
      <div class="logo">✦</div>
      <div class="brand-text"><strong>Meta RC Pulse</strong><span>For Builders Sales</span></div>
    </div>
    <div class="nav-actions">
      <a class="ghost" href="#sample">投資家向けサンプル</a>
      <a class="primary" href="#plans">料金を見る</a>
    </div>
  </nav>

  <button class="voice-btn" onclick="toggleVoicePanel()">🎙 言葉で聞いてみる</button>
  <div id="voicePanel" class="voice-panel">
    <h3>AIに言葉で聞いてみる</h3>
    <p>このページの内容をAIが音声で説明します。気になることを、そのまま言葉で質問できます。</p>
    <button class="primary" onclick="readCurrentSlide()">このページを読み上げる</button>
    <button onclick="alert('音声質問機能は現在準備中です。将来、音声認識とAI対話APIに接続します。')">質問してみる</button>
    <button onclick="toggleVoicePanel()">閉じる</button>
  </div>

  <main class="app" id="app">
    <section class="slide" id="hero" data-read="住所を聞いた瞬間、商談が動き出す。メタRCパルスは、住所を聞いたその場から、法規、最大ボリューム、3DCG没入体験、提案平面図、立面図、概算積算、収益提案までを組み立てる、建設会社営業マン向けのAI営業支援システムです。">
      <div class="inner">
        <div class="pill">契約決定までをパルスコースで完結</div>
        <h1 style="margin-top:18px;">住所を聞いた瞬間、<br><span class="grad">商談が動き出す。</span></h1>
        <p class="lead">建設会社の営業マンが、住所を聞いたその場から法規・最大ボリューム・3DCG没入体験・提案平面図・立面図・概算積算・収益提案までを組み立てるためのAI営業支援システム。</p>
        <div class="actions">
          <a class="btn primary" href="#demo">初回商談で刺さる提案を作る →</a>
          <a class="btn" href="#sample">投資家向け提案サンプルを見る</a>
        </div>
      </div>
      <div class="scroll-indicator">Scroll<span>⌄</span></div>
    </section>

    <section class="slide" id="pain" data-read="もう、設計に確認してから返しますで、投資家の熱を逃がさない。土地を見ても何が建つか言えない。法規が怖い。概算が出せない。収益提案まで踏み込めない。そんな営業現場の待ち時間を、提案時間に変えます。">
      <div class="inner">
        <div class="kicker">Pain Points</div>
        <h2>もう「設計に確認してから返します」で、<span class="grad">投資家の熱を逃がさない。</span></h2>
        <div class="grid three">
          <div class="card center"><h3>何が建つか言えない</h3><p>土地を聞いても、その場で可能性を語れない。</p></div>
          <div class="card center"><h3>法規が怖い</h3><p>用途地域・容積率・道路条件の説明に踏み込めない。</p></div>
          <div class="card center"><h3>概算が出せない</h3><p>工事費や収益感を出せず、商談の熱が下がる。</p></div>
          <div class="card center"><h3>収益説明が弱い</h3><p>投資家が欲しい月商・分配・利回りまで届かない。</p></div>
          <div class="card center"><h3>資料が遅い</h3><p>3DCG・提案図面・収益表の作成に時間がかかる。</p></div>
          <div class="card center"><h3>競合に先を越される</h3><p>設計部に聞く前に、投資家の興味が薄れてしまう。</p></div>
        </div>
      </div>
    </section>

    <section class="slide" id="solution" data-read="営業マンの初期提案力を、建築士へ渡せるレベルへ。住所入力から無料情報取得、5点照合、最大ボリューム算出、3DCG没入体験、提案平面図と立面図、概算積算、収益提案へつなぎます。">
      <div class="inner">
        <div class="kicker">Solution</div>
        <h2>営業マンの初期提案力を、<span class="grad">建築士へ渡せるレベルへ。</span></h2>
        <div class="flow">
          <div class="flow-item">住所入力</div><div class="arrow">→</div>
          <div class="flow-item">無料情報取得</div><div class="arrow">→</div>
          <div class="flow-item">5点照合</div><div class="arrow">→</div>
          <div class="flow-item">最大ボリューム</div><div class="arrow">→</div>
          <div class="flow-item">3DCG没入体験</div><div class="arrow">→</div>
          <div class="flow-item">提案平面図・立面図</div><div class="arrow">→</div>
          <div class="flow-item">概算積算</div><div class="arrow">→</div>
          <div class="flow-item">収益提案</div>
        </div>
        <p class="lead">公的情報優先、5点照合、安全型の緩和採用。正式確定は専門家へつなぎます。</p>
      </div>
    </section>

    <section class="slide" id="pulse" data-read="パルスコースは月額九千八百円。契約決定までの営業導線をパルスコースで完結します。3DCG没入体験、提案平面図、立面図、概算積算、収益シミュレーション、投資家向け提案書生成まで含みます。">
      <div class="inner">
        <div class="kicker">Pulse Course</div>
        <h2>契約決定までの営業導線を、<span class="grad">パルスコースで完結。</span></h2>
        <div class="grid two">
          <div class="card">
            <span class="pill">契約決定まで</span>
            <h3 style="font-size:30px;margin-top:18px;">パルスコース</h3>
            <div class="price">9,800円<small>/月</small></div>
            <p>営業マンが、初回商談から契約決定までの流れを作るための営業完結プラン。</p>
          </div>
          <div class="card">
            <h3>含まれる内容</h3>
            <ul>
              <li>住所入力からの初期提案支援</li>
              <li>用途地域・建ぺい率・容積率などの初期チェック</li>
              <li>3DCG没入体験</li>
              <li>提案平面図・立面図</li>
              <li>概算積算・収益シミュレーション</li>
              <li>投資家向け提案書生成</li>
              <li>銀行融資サポートの入口</li>
              <li>商談用トークスクリプト</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="slide" id="premium" data-read="プレミアムコースは月額九万八千円。契約後の実務作業を支えます。工程管理、建築確認申請サポート、業者への発注手配、承諾催促、ARグラスによる現場遠隔管理指導、中間検査対策、引き渡し保証書類サポートまで対応します。">
      <div class="inner">
        <div class="kicker">Premium Course</div>
        <h2>契約後の実務作業を、<span class="grad">プレミアムコースで支える。</span></h2>
        <div class="grid two">
          <div class="card">
            <span class="pill">契約後の実務支援</span>
            <h3 style="font-size:30px;margin-top:18px;">プレミアムコース</h3>
            <div class="price">98,000円<small>/月</small></div>
            <p>契約後の実務作業を、建築会社の現場運営・確認・発注・引き渡しまで支えるサポートプラン。</p>
          </div>
          <div class="card">
            <h3>含まれる内容</h3>
            <ul>
              <li>パルスコースの内容すべて</li>
              <li>工程管理サポート</li>
              <li>建築確認申請サポート</li>
              <li>業者への発注手配・承諾催促</li>
              <li>ARグラスによる現場遠隔管理指導</li>
              <li>中間検査対策</li>
              <li>引き渡し保証書類サポート</li>
              <li>実務進行の抜け漏れチェック</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="slide" id="sample" data-read="この完成提案を、あなたの営業現場で出せます。たとえばメタRCミュージックラボマンション。地上は住居収益、地下はSNSクリエイター向け配信ラボ。投資家に欲しいと思わせる完成イメージを初回商談で提示できます。">
      <div class="inner">
        <div class="kicker">Investor Sample</div>
        <h2>この完成提案を、<span class="grad">あなたの営業現場で出せます。</span></h2>
        <p class="lead">たとえば、Meta RC Music Lab Mansion。地上は住居収益、地下はSNSクリエイター向け配信ラボ。まず3DCG没入体験で心を動かし、次に提案平面図・立面図・概算積算・収益表で契約判断へ進めます。</p>
        <div class="actions">
          <a class="btn primary" href="#demo">住所から提案を作る</a>
          <a class="btn" href="javascript:void(0)" onclick="alert('投資家向けページ /investor は次の段階で接続します。')">投資家向け提案サンプルを見る</a>
        </div>
      </div>
    </section>

    <section class="slide" id="demo" data-read="まずは一件、住所から商談を動かす。住所と頭金から、投資家の目が変わる初期提案の流れを体験してください。">
      <div class="inner">
        <div class="kicker">Final CTA</div>
        <h2>まずは1件、<span class="grad">住所から商談を動かす。</span></h2>
        <form class="form" onsubmit="event.preventDefault(); alert('デモ送信です。次の段階で無料情報取得、5点照合、3DCG没入体験、提案平面図・立面図、概算積算、収益提案書生成エンジンに接続します。');">
          <label>希望建築地住所</label>
          <input name="desired_building_address" value="東京都港区六本木1丁目1-1" oninput="this.setAttribute('value', this.value)" />
          <label>頭金</label>
          <input value="100万円" oninput="this.setAttribute('value', this.value)" />
          <button class="btn primary" style="width:100%;border:0;cursor:pointer;" type="submit">希望建築地住所を入れて、商談を動かす →</button>
          <div class="note">このフォームはLP用デモです。実装時は無料情報取得、5点照合、3DCG没入体験、提案平面図・立面図、概算積算、収益提案書生成エンジンと接続します。</div>
        </form>
      </div>
    </section>
  </main>

  <div class="switcher" aria-hidden="true">
    <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
  </div>

  <script>
    function toggleVoicePanel(){
      document.getElementById('voicePanel').classList.toggle('open');
    }
    function getCurrentSlide(){
      const slides = Array.from(document.querySelectorAll('.slide'));
      const middle = window.innerHeight / 2;
      let current = slides[0];
      let best = Infinity;
      slides.forEach(s => {
        const r = s.getBoundingClientRect();
        const dist = Math.abs((r.top + r.height/2) - middle);
        if(dist < best){ best = dist; current = s; }
      });
      return current;
    }
    function readCurrentSlide(){
      const slide = getCurrentSlide();
      const text = slide.getAttribute('data-read') || slide.innerText;
      if(!('speechSynthesis' in window)){
        alert('このブラウザでは読み上げ機能が利用できません。');
        return;
      }
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = 'ja-JP';
      utter.rate = 0.92;
      utter.pitch = 1.0;
      window.speechSynthesis.speak(utter);
    }
  </script>
</body>
</html>
"""

components.html(HTML, height=900, scrolling=True)


# AGP_REAL_FORM_V1
# 宇宙型LPの下に、本物送信用フォームを追加します。
import os
from datetime import datetime, timezone

try:
    import requests
except Exception:
    requests = None


def agp_get_secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    if not value:
        value = os.environ.get(name, "")
    return str(value).strip()


def agp_send_to_sheet(payload: dict) -> dict:
    url = agp_get_secret("APPS_SCRIPT_WEB_APP_URL")
    if not url:
        return {
            "ok": None,
            "message": "外部保存URLが未接続です。Streamlit Secrets に APPS_SCRIPT_WEB_APP_URL を設定してください。",
        }

    if requests is None:
        return {
            "ok": False,
            "message": "送信ライブラリを確認中です。",
        }

    try:
        response = requests.post(url, json=payload, timeout=12)
        try:
            result = response.json()
        except ValueError:
            result = {}

        if response.ok and result.get("ok") is True:
            return result

        return {
            "ok": False,
            "message": result.get("message") or "外部保存に失敗しました。",
        }
    except Exception:
        return {
            "ok": False,
            "message": "外部保存に失敗しました。",
        }


st.markdown(
    """
    <style>
    .agp-real-wrap {
        max-width: 760px;
        margin: 0 auto 80px;
        padding: 0 18px;
    }
    .agp-real-card {
        border: 1px solid rgba(84,216,255,.28);
        background: linear-gradient(180deg, rgba(3,8,20,.94), rgba(4,12,28,.86));
        box-shadow: 0 0 70px rgba(84,216,255,.16), 0 24px 90px rgba(0,0,0,.42);
        border-radius: 30px;
        padding: 28px;
        color: white;
    }
    .agp-real-card h2 {
        margin: 0 0 10px;
        font-size: clamp(28px, 5vw, 48px);
        letter-spacing: -0.04em;
    }
    .agp-real-card p {
        color: rgba(226,238,255,.78);
        line-height: 1.9;
        margin: 0 0 22px;
    }
    .stButton button {
        width: 100%;
        border: 0 !important;
        border-radius: 999px !important;
        padding: 0.9rem 1.2rem !important;
        font-weight: 900 !important;
        color: #00131d !important;
        background: linear-gradient(135deg, #5fffd2, #54d8ff, #337dff) !important;
        box-shadow: 0 0 40px rgba(84,216,255,.22) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="agp-real-wrap"><div class="agp-real-card"><h2>本物送信用フォーム</h2><p>希望建築地住所を入れると、Googleスプレッドシート保存ルートへ送信します。</p>',
    unsafe_allow_html=True,
)

with st.form("agp_real_registration_form", clear_on_submit=False):
    name = st.text_input("お名前", value="テスト 太郎")
    email = st.text_input("メールアドレス", value="test@example.com")
    desired_building_address = st.text_input("希望建築地住所", value="東京都港区六本木1丁目1-1")
    country = st.text_input("国", value="日本")
    company = st.text_input("会社名", value="テスト建設")
    preferred_language = st.selectbox("希望言語", ["日本語", "English", "中文", "한국어", "Español"])
    is_builder_sales = st.checkbox("建築営業マンですか？", value=True)
    wants_demo = st.checkbox("デモ予約も希望する", value=True)

    submitted = st.form_submit_button("希望建築地住所を入れて、商談を動かす →")

if submitted:
    payload = {
        "source": "meta-rc-pulse-streamlit-cosmic-lp",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "name": name.strip(),
        "email": email.strip(),
        "desired_building_address": desired_building_address.strip(),
        "希望建築地住所": desired_building_address.strip(),
        "address": desired_building_address.strip(),
        "phone": desired_building_address.strip(),
        "country": country.strip(),
        "company": company.strip(),
        "preferred_language": preferred_language,
        "is_builder_sales": "はい" if is_builder_sales else "いいえ",
        "builder_sales": "はい" if is_builder_sales else "いいえ",
        "建築営業マン": "はい" if is_builder_sales else "いいえ",
        "wants_demo": "はい" if wants_demo else "いいえ",
        "demo_requested": "はい" if wants_demo else "いいえ",
        "デモ予約希望": "はい" if wants_demo else "いいえ",
    }

    result = agp_send_to_sheet(payload)

    if result.get("ok") is True:
        st.success(result.get("message") or "Googleスプレッドシートへ保存しました")
        if result.get("mail_sent"):
            st.info("自動返信メールを送信しました")
        if result.get("admin_mail_sent"):
            st.info("管理者通知メールを送信しました")
    elif result.get("ok") is None:
        st.warning(result.get("message") or "外部保存URLが未接続です")
    else:
        st.error(result.get("message") or "外部保存に失敗しました")

st.markdown("</div></div>", unsafe_allow_html=True)



