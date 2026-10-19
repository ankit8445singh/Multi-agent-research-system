import time

import streamlit as st

from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain


st.set_page_config(
    page_title="ResearchMind",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

        :root { --ink:#d8e7f0; --muted:#78919e; --line:rgba(92,196,214,.16); --card:rgba(6,18,25,.88); --cyan:#4de7f5; --violet:#55a9ff; --success:#61e8ac; }
        .stApp { background: #03080c; color: var(--ink); }
        .stApp:before { content:""; position:fixed; inset:0; pointer-events:none; background:radial-gradient(ellipse 60% 35% at 50% -15%, rgba(20,138,167,.18), transparent 65%), radial-gradient(circle at 95% 14%, rgba(30,110,148,.10), transparent 24%), linear-gradient(rgba(77,231,245,.025) 1px, transparent 1px), linear-gradient(90deg, rgba(77,231,245,.025) 1px, transparent 1px); background-size:auto,auto,32px 32px,32px 32px; }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { max-width:1280px; padding:1.4rem 2.5rem 4rem; }
        html, body, [class*="css"] { font-family:Manrope, sans-serif; }

        .topbar { display:flex; align-items:center; justify-content:space-between; margin-bottom:3.5rem; }
        .brand { display:flex; align-items:center; gap:.72rem; font-family:'DM Mono',monospace; font-size:.88rem; font-weight:500; letter-spacing:.06em; }
        .brand-mark { width:34px; height:34px; display:grid; place-items:center; border:1px solid rgba(77,231,245,.55); border-radius:4px; color:#9bf6ff; background:rgba(77,231,245,.08); box-shadow:inset 0 0 18px rgba(77,231,245,.08),0 0 28px rgba(77,231,245,.13); }
        .nav-label, .eyebrow, .section-kicker, .agent-meta { font-family:'DM Mono', monospace; font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; }
        .nav-label { color:var(--muted); }
        .status-pill { display:flex; align-items:center; gap:.45rem; padding:.42rem .7rem; border:1px solid var(--line); border-radius:999px; color:#c2cbe0; background:rgba(255,255,255,.025); font-size:.72rem; }
        .status-dot { width:7px; height:7px; border-radius:50%; background:var(--success); box-shadow:0 0 10px var(--success); }

        .hero { max-width:830px; margin:0 auto 3rem; text-align:center; }
        .eyebrow { color:var(--cyan); margin-bottom:1.05rem; }
        .hero h1 { margin:0; font-family:'DM Mono',monospace; font-size:clamp(2rem,4.6vw,4.5rem); letter-spacing:-.065em; line-height:1.12; font-weight:500; background:linear-gradient(120deg,#e9f9fb 18%,#6eeefa 55%,#81bcff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .hero p { max-width:590px; margin:1.25rem auto 0; color:var(--muted); font-size:1rem; line-height:1.75; }

        .workspace { padding:1.2rem; border:1px solid var(--line); border-radius:7px; background:linear-gradient(145deg,rgba(7,24,32,.94),rgba(3,11,16,.96)); box-shadow:inset 0 1px 0 rgba(176,245,255,.06),0 20px 70px rgba(0,0,0,.42); }
        .workspace-title { display:flex; justify-content:space-between; align-items:center; padding:.2rem .35rem 1rem; }
        .workspace-title strong { font-size:.95rem; }
        .section-kicker { color:var(--muted); }
        .stTextInput label { font-family:'DM Mono',monospace!important; font-size:.68rem!important; letter-spacing:.12em!important; text-transform:uppercase!important; color:#aebad2!important; }
        .stTextInput input { background:rgba(3,8,22,.48)!important; color:var(--ink)!important; border:1px solid rgba(147,165,209,.22)!important; border-radius:12px!important; min-height:50px!important; padding:0 1rem!important; }
        .stTextInput input:focus { border-color:var(--cyan)!important; box-shadow:0 0 0 3px rgba(98,213,255,.12)!important; }
        .stButton button { height:50px; border:1px solid rgba(135,246,255,.8)!important; border-radius:5px!important; font-family:'DM Mono',monospace!important; font-size:.78rem!important; letter-spacing:.08em!important; font-weight:500!important; color:#001114!important; background:linear-gradient(120deg,#72f0fa,#59aaff)!important; box-shadow:0 10px 26px rgba(77,231,245,.18)!important; transition:transform .16s ease, box-shadow .16s ease!important; }
        .stButton button:hover { transform:translateY(-2px); box-shadow:0 14px 34px rgba(98,213,255,.30)!important; }
        .hint { margin:.9rem .2rem 0; color:#72809a; font-size:.76rem; }

        .pipeline-card { height:100%; padding:.85rem .85rem .2rem; border-left:1px solid var(--line); }
        .agent { display:flex; gap:.85rem; align-items:flex-start; padding:1rem .8rem; border-radius:4px; margin-bottom:.4rem; }
        .agent.active { background:rgba(98,213,255,.075); border:1px solid rgba(98,213,255,.18); }
        .agent.done { background:rgba(99,223,164,.055); }
        .agent-icon { flex:0 0 32px; width:32px; height:32px; display:grid; place-items:center; border-radius:10px; background:rgba(255,255,255,.055); font-size:.9rem; }
        .agent h4 { margin:0 0 .18rem; font-size:.82rem; }
        .agent p { margin:0; color:#8090ab; font-size:.7rem; line-height:1.45; }
        .agent-status { margin-left:auto; padding-top:.2rem; color:#8290a8; font-family:'DM Mono',monospace; font-size:.58rem; letter-spacing:.06em; }
        .agent.active .agent-status { color:var(--cyan); } .agent.done .agent-status { color:var(--success); }
        .stProgress > div > div > div { background:linear-gradient(90deg,var(--cyan),var(--violet))!important; }

        .result-head { margin:3rem 0 1rem; display:flex; align-items:end; justify-content:space-between; }
        .result-head h2 { margin:.25rem 0 0; font-size:1.65rem; letter-spacing:-.04em; }
        .report-shell { padding:1.8rem 2rem; border:1px solid rgba(77,231,245,.22); border-radius:5px; background:rgba(5,17,24,.88); }
        .report-shell h1, .report-shell h2, .report-shell h3 { color:#eaf5ff; letter-spacing:-.035em; }
        .report-shell p, .report-shell li { color:#bdc8dc; line-height:1.8; }
        .feedback { padding:1.5rem 1.75rem; border:1px solid rgba(99,223,164,.20); border-radius:5px; background:rgba(9,33,31,.48); }
        .feedback h1, .feedback h2, .feedback h3 { color:#b7f4d4; }
        .feedback p, .feedback li { color:#bfd8cc; line-height:1.75; }
        .stExpander { border:1px solid var(--line)!important; border-radius:12px!important; background:rgba(255,255,255,.02)!important; }
        .stDownloadButton button { border:1px solid rgba(98,213,255,.42)!important; border-radius:10px!important; color:#b9edff!important; background:transparent!important; }
        @media(max-width:800px) { .block-container { padding:1rem 1rem 3rem; } .topbar { margin-bottom:2.3rem; } .pipeline-card { border-left:0; border-top:1px solid var(--line); margin-top:1.1rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def agent_card(icon: str, title: str, description: str, status: str) -> None:
    state = "done" if status == "Complete" else "active" if status == "Working" else ""
    st.markdown(
        f'''<div class="agent {state}"><div class="agent-icon">{icon}</div><div><h4>{title}</h4><p>{description}</p></div><div class="agent-status">{status}</div></div>''',
        unsafe_allow_html=True,
    )


def render_pipeline(results: dict, running_step: str | None = None) -> None:
    labels = [
        ("search", "⌕", "Search intelligence", "Finds credible, current sources"),
        ("reader", "◫", "Deep reader", "Extracts context from the best source"),
        ("writer", "✎", "Research writer", "Builds a structured report"),
        ("critic", "◈", "Quality reviewer", "Checks clarity and completeness"),
    ]
    for key, icon, title, description in labels:
        status = "Complete" if key in results else "Working" if key == running_step else "Queued"
        agent_card(icon, title, description, status)


def run_pipeline(topic: str, status_slot, pipeline_slot) -> None:
    results: dict[str, str] = {}
    stages = [
        ("search", "[01/04] Acquiring verified source signals…"),
        ("reader", "[02/04] Parsing high-relevance source material…"),
        ("writer", "[03/04] Synthesizing technical briefing…"),
        ("critic", "[04/04] Running quality-validation pass…"),
    ]
    progress = st.progress(0, text="Initializing orchestration layer…")

    try:
        for index, (stage, message) in enumerate(stages, start=1):
            status_slot.info(message)
            with pipeline_slot.container():
                render_pipeline(results, stage)

            if stage == "search":
                response = build_search_agent().invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
                results["search"] = response["messages"][-1].content
            elif stage == "reader":
                response = build_reader_agent().invoke({"messages": [("user", f"Based on these search results about '{topic}', pick the most relevant URL and extract deeper content.\n\n{results['search'][:800]}")]})
                results["reader"] = response["messages"][-1].content
            elif stage == "writer":
                research = f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED CONTENT:\n{results['reader']}"
                results["writer"] = writer_chain.invoke({"topic": topic, "research": research})
            else:
                results["critic"] = critic_chain.invoke({"report": results["writer"]})

            progress.progress(index / len(stages), text=f"{stage.upper()} NODE: COMPLETE")

        st.session_state.results = results
        status_slot.success("PIPELINE COMPLETE — briefing available in output buffer.")
    except Exception as error:
        status_slot.error(f"PIPELINE INTERRUPTION: {error}")
    finally:
        st.session_state.running = False
        with pipeline_slot.container():
            render_pipeline(st.session_state.get("results", results))


inject_styles()
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False

st.markdown('''<div class="topbar"><div class="brand"><span class="brand-mark">◈</span>RESEARCHMIND / CORE</div><div class="status-pill"><span class="status-dot"></span>AGENT NETWORK: ONLINE</div></div>''', unsafe_allow_html=True)
st.markdown('''<section class="hero"><div class="eyebrow">Autonomous intelligence system · v1.0</div><h1>Research, decoded.</h1><p>Deploy a coordinated set of AI agents to search, analyze, synthesize, and validate a technical research briefing.</p></section>''', unsafe_allow_html=True)

st.markdown('<div class="workspace">', unsafe_allow_html=True)
left, right = st.columns([1.25, 0.95], gap="large")
with left:
    st.markdown('<div class="workspace-title"><div><div class="section-kicker">Query console</div><strong>Initialize research task</strong></div><span class="nav-label">NODE_01</span></div>', unsafe_allow_html=True)
    topic = st.text_input("Target subject", placeholder="e.g., The state of fusion energy in 2026", label_visibility="visible")
    run = st.button("▶ EXECUTE RESEARCH", use_container_width=True, disabled=st.session_state.running)
    st.markdown('<p class="hint">PARAMETERS: Include timeframe, region, or technical focus to improve precision.</p>', unsafe_allow_html=True)
    status_slot = st.empty()

with right:
    st.markdown('<div class="pipeline-card"><div class="workspace-title"><div><div class="section-kicker">Process monitor</div><strong>Agent orchestration</strong></div></div>', unsafe_allow_html=True)
    pipeline_slot = st.empty()
    with pipeline_slot.container():
        render_pipeline(st.session_state.results)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if run:
    if not topic.strip():
        status_slot.warning("INPUT REQUIRED: Specify a target subject before execution.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        run_pipeline(topic.strip(), status_slot, pipeline_slot)

results = st.session_state.results
if results:
    st.markdown('<div class="result-head"><div><div class="section-kicker">Output buffer</div><h2>Research briefing generated</h2></div></div>', unsafe_allow_html=True)
    report_tab, review_tab, sources_tab = st.tabs(["SYNTHESIS REPORT", "VALIDATION LOG", "SOURCE TRACE"])
    with report_tab:
        st.markdown('<div class="report-shell">', unsafe_allow_html=True)
        st.markdown(results.get("writer", ""))
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("↓ EXPORT REPORT (.MD)", results.get("writer", ""), f"research_brief_{int(time.time())}.md", "text/markdown")
    with review_tab:
        st.markdown('<div class="feedback">', unsafe_allow_html=True)
        st.markdown(results.get("critic", "No review was produced."))
        st.markdown('</div>', unsafe_allow_html=True)
    with sources_tab:
        with st.expander("Search-agent notes", expanded=True):
            st.text(results.get("search", ""))
        with st.expander("Reader-agent notes"):
            st.text(results.get("reader", ""))
