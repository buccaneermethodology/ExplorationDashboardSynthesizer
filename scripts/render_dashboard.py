#!/usr/bin/env python3
"""Render an Exploration Dashboard JSON/Markdown document as a standalone HTML view."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


def text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, list):
        return "; ".join(text(item) for item in value)
    return str(value)


def list_value(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [text(item) for item in value if text(item)]
    return [text(value)] if text(value) else []


def normalize(data: dict[str, Any]) -> dict[str, Any]:
    """Accept the documented schema while remaining tolerant of simple aliases."""
    out = dict(data)
    out.setdefault("schema_version", "exploration_dashboard_v1")
    out.setdefault("title", "Exploration Dashboard")
    out.setdefault("subtitle", "由 Exploration Dashboard Synthesizer 生成的可筛选离线视图")
    out.setdefault("generated_on", date.today().isoformat())
    out["big_ideas"] = list(data.get("big_ideas", data.get("bigIdeas", [])))
    out["stage_plans"] = list(data.get("stage_plans", data.get("stagePlans", [])))
    out["sessions"] = list(data.get("sessions", []))
    out["recommendations"] = list(data.get("recommendations", data.get("next_suggestions", [])))
    out["source_manifest"] = list(data.get("source_manifest", []))
    for i, idea in enumerate(out["big_ideas"], 1):
        idea.setdefault("id", f"B{i}")
        idea.setdefault("topic", idea.get("name", idea.get("title", idea["id"])))
        idea.setdefault("status", "")
        idea.setdefault("key_points", [])
        idea.setdefault("next_suggestions", [])
    for i, plan in enumerate(out["stage_plans"], 1):
        plan.setdefault("id", f"SP-{i:03d}")
        plan.setdefault("topic", plan.get("name", plan.get("title", plan["id"])))
        plan.setdefault("status", "")
        plan.setdefault("big_ideas", plan.get("bis", []))
    for i, session in enumerate(out["sessions"], 1):
        session.setdefault("id", f"S-{i:03d}")
        session.setdefault("type", session.get("session_type", "Exploration"))
        session.setdefault("topic", session.get("title", session["id"]))
        session.setdefault("status", "")
        session.setdefault("priority", "")
        session.setdefault("big_ideas", session.get("tracks", session.get("bi", [])))
        session.setdefault("stage_plan", session.get("parent", ""))
        session.setdefault("phase_tags", [])
        session.setdefault("surface", "")
        session.setdefault("key_points", [])
    return out


def parse_markdown(source: str) -> dict[str, Any]:
    """Parse the standard Markdown output into the renderer schema.

    The parser intentionally keeps only stable fields from the standard table. For
    richer views, callers should provide the JSON schema documented in the reference.
    """
    data: dict[str, Any] = {"title": "Exploration Dashboard", "big_ideas": [], "sessions": []}
    blocks = re.split(r"(?m)^## Big Idea:\s*", source)
    for index, block in enumerate(blocks[1:], 1):
        lines = block.splitlines()
        topic = lines[0].strip() or f"Big Idea {index}"
        idea: dict[str, Any] = {"id": f"B{index}", "topic": topic, "key_points": [], "next_suggestions": []}
        current = None
        for line in lines:
            match = re.match(r"^- Big Idea Length:\s*(.*)", line)
            if match:
                idea["length"] = match.group(1).strip()
            match = re.match(r"^- Coverage:\s*(.*)", line)
            if match:
                idea["coverage"] = match.group(1).strip()
            if line.strip() == "- Key Points:":
                current = idea["key_points"]
            elif line.strip() == "- Next Suggestions:":
                current = idea["next_suggestions"]
            elif line.startswith("  - ") and current is not None:
                current.append(line[4:].strip())
        table_match = re.search(r"(?ms)^\| Session ID \|.*?\n\|[-| ]+\|\n(?P<rows>(?:\|.*\n?)*)", block)
        if table_match:
            for row in table_match.group("rows").splitlines():
                cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
                if len(cells) < 7 or not cells[0] or cells[0].startswith("---"):
                    continue
                session = {
                    "id": cells[0], "type": cells[1], "topic": cells[2], "scope": cells[3],
                    "purpose": cells[4], "length": cells[5], "key_points": [cells[6]],
                    "big_ideas": [idea["id"]],
                }
                data["sessions"].append(session)
        data["big_ideas"].append(idea)
    return normalize(data)


def load_input(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return normalize(json.loads(raw))
    return parse_markdown(raw)


def json_script(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


HTML_TEMPLATE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--ink:#182238;--muted:#667085;--line:#dfe5ef;--brand:#3758d3;--good:#16804d;--warn:#a56300;--bad:#b42318;--shadow:0 12px 32px rgba(37,52,90,.08)}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:linear-gradient(145deg,#eef3ff,#f8fafc 38%,#f5f0ff);font:14px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.shell{max-width:1500px;margin:auto;padding:28px}.hero,.panel{background:rgba(255,255,255,.96);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow)}.hero{padding:30px}.hero h1{font-size:clamp(28px,4vw,48px);line-height:1.12;margin:0 0 10px}.lede{font-size:17px;color:#3e4a61;max-width:980px}.subtle{color:var(--muted)}.tabs{position:sticky;top:0;z-index:20;display:flex;gap:8px;margin:18px 0;padding:10px;background:rgba(244,247,251,.92);backdrop-filter:blur(12px);border:1px solid var(--line);border-radius:16px}.tabs button,.btn{border:0;border-radius:11px;padding:10px 14px;background:#fff;color:var(--ink);cursor:pointer;font-weight:700}.tabs button.active{background:var(--brand);color:#fff}.panel{padding:20px;margin:18px 0}.section-title{display:flex;align-items:end;justify-content:space-between;gap:16px;margin-bottom:16px}.section-title h2{margin:0;font-size:22px}.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:9px;align-items:end}.filters .search{grid-column:span 2}.filters label{display:grid;gap:4px;color:var(--muted);font-size:12px;font-weight:700}.filters input,.filters select{width:100%;padding:10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}.metrics,.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.metric,.card{padding:16px;border:1px solid var(--line);border-radius:16px;background:#fff}.metric b{display:block;font-size:25px;line-height:1.1}.metric span{color:var(--muted);font-size:12px}.card h3{margin:4px 0 6px;font-size:18px}.tag{display:inline-flex;border-radius:999px;padding:4px 9px;background:#eef2ff;color:#3447a5;font-size:12px;font-weight:700;margin:2px}.status-Done{background:#e8f7ef;color:var(--good)}.status-Doing{background:#fff2d8;color:var(--warn)}.status-To-do{background:#e8f1ff;color:#2457a6}.status-Cancelled{background:#fbe9e7;color:var(--bad)}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:14px}table{border-collapse:collapse;width:100%;min-width:950px}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{position:sticky;top:0;background:#f6f8fc;font-size:12px;color:var(--muted)}tr:hover td{background:#fafbff}.link-button{border:0;background:none;padding:0;color:var(--brand);font:inherit;font-weight:800;cursor:pointer;text-align:left}.pager{display:flex;align-items:center;justify-content:space-between;margin-top:12px}.controls{display:flex;gap:8px}.drawer{position:fixed;inset:0;z-index:60;background:rgba(21,28,44,.48);display:none;justify-content:flex-end}.drawer.open{display:flex}.drawer-card{height:100%;width:min(720px,94vw);overflow:auto;background:#fff;padding:26px;box-shadow:-16px 0 40px rgba(0,0,0,.16)}.drawer-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}.drawer-head h2{margin:0}.close{border:0;background:#eef1f6;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:20px}.detail-grid{display:grid;grid-template-columns:140px 1fr;gap:9px 14px;margin-top:20px}.detail-grid dt{color:var(--muted);font-weight:700}.detail-grid dd{margin:0;white-space:pre-wrap;overflow-wrap:anywhere}.empty{text-align:center;padding:48px;color:var(--muted)}@media(max-width:720px){.shell{padding:12px}.hero{padding:20px}.filters,.grid,.metrics{grid-template-columns:1fr}.filters .search{grid-column:auto}.tabs{overflow:auto}.tabs button{white-space:nowrap}.detail-grid{grid-template-columns:1fr}}
</style></head><body><main class="shell"><section class="hero"><div class="subtle">EXPLORATION DASHBOARD</div><h1>__TITLE__</h1><p class="lede">__SUBTITLE__</p><div class="metrics" id="metrics"></div></section>
<nav class="tabs" aria-label="Dashboard views"><button data-view="overview" class="active">全景总览</button><button data-view="bi">大方向（BI）</button><button data-view="sp">执行批次（SP）</button><button data-view="session">全部 Sessions</button><button data-view="source">数据口径</button></nav>
<section class="panel" id="filter-panel"><div class="section-title"><div><h2>筛选器</h2><p class="subtle">筛选只改变当前视图，不改变源数据。</p></div><strong id="result-count" aria-live="polite"></strong></div><div class="filters"><label class="search">关键词<input id="q" type="search" placeholder="搜索 ID、主题、范围、目的或要点"></label><label>状态<select id="status"><option value="">全部状态</option></select></label><label>Session 类型<select id="type"><option value="">全部类型</option></select></label><label>Big Idea<select id="bi"><option value="">全部 BI</option></select></label><label>Stage Plan<select id="sp"><option value="">全部 SP</option></select></label><label>当前/归档<select id="surface"><option value="">全部表面</option><option value="current">当前表</option><option value="archive">历史归档</option></select></label><label>阶段<select id="phase"><option value="">全部阶段</option></select></label><label>排序<select id="sort"><option value="source">源顺序</option><option value="id">ID</option><option value="status">状态</option><option value="priority">优先级</option></select></label><button class="btn" id="reset">清空</button></div></section>
<div id="view"></div></main><aside class="drawer" id="drawer" aria-hidden="true"><div class="drawer-card"><div class="drawer-head"><div><span class="tag" id="drawer-kind"></span><h2 id="drawer-title"></h2></div><button class="close" id="drawer-close" aria-label="关闭">×</button></div><dl class="detail-grid" id="drawer-detail"></dl></div></aside>
<script id="dashboard-data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.getElementById('dashboard-data').textContent),$=id=>document.getElementById(id),state={view:'overview',page:1,pageSize:20};
const filters={q:$('q'),status:$('status'),type:$('type'),bi:$('bi'),sp:$('sp'),surface:$('surface'),phase:$('phase')},sortSelect=$('sort');
const allItems=()=>[...data.big_ideas,...data.stage_plans,...data.sessions],uniq=a=>[...new Set(a.flatMap(x=>Array.isArray(x)?x:[x]).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b),'zh-CN',{numeric:true}));
const addOptions=(el,values)=>uniq(values).forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;el.appendChild(o)});
addOptions(filters.status,allItems().map(x=>x.status));addOptions(filters.type,data.sessions.map(x=>x.type));addOptions(filters.bi,data.big_ideas.map(x=>x.id));addOptions(filters.sp,data.stage_plans.map(x=>x.id));addOptions(filters.phase,allItems().map(x=>x.phase_tags||[]));
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),arr=v=>Array.isArray(v)?v:(v?[v]:[]),badge=v=>v?`<span class="tag status-${esc(String(v).replaceAll(' ','-'))}">${esc(v)}</span>`:'';
function readHash(){const p=new URLSearchParams(location.hash.slice(1));if(['overview','bi','sp','session','source'].includes(p.get('view')))state.view=p.get('view');state.page=Math.max(1,Number(p.get('page')||1));Object.entries(filters).forEach(([k,e])=>{if(p.has(k))e.value=p.get(k)});if(p.has('sort'))sortSelect.value=p.get('sort')}
function writeHash(){const p=new URLSearchParams({view:state.view});if(state.page>1)p.set('page',state.page);Object.entries(filters).forEach(([k,e])=>{if(e.value)p.set(k,e.value)});if(sortSelect.value!=='source')p.set('sort',sortSelect.value);history.replaceState(null,'',`#${p}`)}
function kindItems(kind){return kind==='bi'?data.big_ideas:kind==='sp'?data.stage_plans:data.sessions}function blob(x){return JSON.stringify(x).toLowerCase()}
function matches(x,kind){const q=filters.q.value.trim().toLowerCase();if(q&&!blob(x).includes(q))return false;if(filters.status.value&&x.status!==filters.status.value)return false;if(filters.type.value&&(kind!=='session'||x.type!==filters.type.value))return false;if(filters.bi.value){const ids=kind==='bi'?[x.id]:kind==='sp'?arr(x.big_ideas):arr(x.big_ideas);if(!ids.includes(filters.bi.value))return false}if(filters.sp.value){if(kind==='sp'&&x.id!==filters.sp.value)return false;if(kind==='session'&&x.stage_plan!==filters.sp.value)return false;if(kind==='bi'&&!arr(x.stage_plans).includes(filters.sp.value))return false}if(filters.surface.value&&kind==='session'&&x.surface!==filters.surface.value)return false;if(filters.phase.value&&!arr(x.phase_tags).includes(filters.phase.value))return false;return true}
function filtered(kind){const out=kindItems(kind).filter(x=>matches(x,kind));if(sortSelect.value==='id')out.sort((a,b)=>a.id.localeCompare(b.id,'zh-CN',{numeric:true}));if(sortSelect.value==='status')out.sort((a,b)=>String(a.status).localeCompare(String(b.status))||a.id.localeCompare(b.id));if(sortSelect.value==='priority')out.sort((a,b)=>String(a.priority||'Z').localeCompare(String(b.priority||'Z'))||a.id.localeCompare(b.id));return out}
function metrics(){const c=[['BI',data.big_ideas.length],['SP',data.stage_plans.length],['Sessions',data.sessions.length],['Exploration',data.sessions.filter(x=>x.type==='Exploration').length],['Knowledge',data.sessions.filter(x=>x.type==='Knowledge').length],['Proposed',data.sessions.filter(x=>x.type==='Proposed').length]];$('metrics').innerHTML=c.map(x=>`<div class="metric"><b>${x[1]}</b><span>${x[0]}</span></div>`).join('')}
function openDetail(kind,id){const x=kindItems(kind).find(y=>y.id===id);if(!x)return;$('drawer-kind').textContent=kind.toUpperCase();$('drawer-title').textContent=`${x.id} · ${x.topic}`;$('drawer-detail').innerHTML=Object.entries(x).filter(([,v])=>v!==''&&v!==null&&v!==undefined).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(Array.isArray(v)?v.join('\n'):typeof v==='object'?JSON.stringify(v,null,2):v)}</dd>`).join('');$('drawer').classList.add('open');$('drawer').setAttribute('aria-hidden','false')}
function cards(kind){const xs=filtered(kind);$('result-count').textContent=`${xs.length} / ${kindItems(kind).length} 条匹配`;return xs.length?`<div class="grid">${xs.map(x=>`<article class="card">${badge(x.status)} <span class="tag">${esc(x.id)}</span><h3>${esc(x.topic)}</h3><p>${esc(x.purpose||x.scope||x.coverage||'')}</p><p class="subtle">${esc(arr(x.key_points).join('；'))}</p><button class="link-button" data-open="${kind}" data-id="${esc(x.id)}">查看详情 →</button></article>`).join('')}</div>`:'<div class="empty">当前筛选没有匹配项。</div>'}
function table(kind){const xs=filtered(kind),pages=Math.max(1,Math.ceil(xs.length/state.pageSize));state.page=Math.min(state.page,pages);const rows=xs.slice((state.page-1)*state.pageSize,state.page*state.pageSize);$('result-count').textContent=`${xs.length} 条匹配 · 第 ${state.page}/${pages}`;const head=kind==='sp'?['ID','状态','Topic','关联 BI','Purpose']:['ID','状态','类型','Big Idea','表面','Topic / Purpose'];return `<div class="table-wrap"><table><thead><tr>${head.map(x=>`<th>${x}</th>`).join('')}</tr></thead><tbody>${rows.map(x=>kind==='sp'?`<tr><td><button class="link-button" data-open="sp" data-id="${esc(x.id)}">${esc(x.id)}</button></td><td>${badge(x.status)}</td><td>${esc(x.topic)}</td><td>${esc(arr(x.big_ideas).join(', '))}</td><td>${esc(x.purpose||x.scope||'')}</td></tr>`:`<tr><td><button class="link-button" data-open="session" data-id="${esc(x.id)}">${esc(x.id)}</button></td><td>${badge(x.status)}</td><td>${esc(x.type)}</td><td>${esc(arr(x.big_ideas).join(', '))}</td><td>${esc(x.surface||'')}</td><td>${esc(x.topic)}<br><span class="subtle">${esc(x.purpose||x.scope||'')}</span></td></tr>`).join('')}</tbody></table></div><div class="pager"><span>每页 ${state.pageSize} 条</span><div class="controls"><button class="btn" data-page="prev" ${state.page<=1?'disabled':''}>上一页</button><button class="btn" data-page="next" ${state.page>=pages?'disabled':''}>下一页</button></div></div>`}
function render(){writeHash();document.querySelectorAll('[data-view]').forEach(x=>x.classList.toggle('active',x.dataset.view===state.view));$('filter-panel').style.display=state.view==='source'?'none':'block';let body='';if(state.view==='overview')body=`<section class="panel"><div class="section-title"><div><h2>大方向</h2><p class="subtle">保留 Big Idea 与 Session 的关系，支持继续下钻。</p></div></div>${cards('bi')}</section><section class="panel"><h2>下一步候选</h2><div class="grid">${data.recommendations.map(x=>`<article class="card"><h3>${esc(x.title||x.topic||x)}</h3><p>${esc(x.detail||x.purpose||'')}</p></article>`).join('')}</div></section>`;else if(state.view==='bi')body=`<section class="panel"><h2>全部 Big Ideas</h2>${cards('bi')}</section>`;else if(state.view==='sp')body=`<section class="panel"><h2>全部 Stage Plans</h2>${table('sp')}</section>`;else if(state.view==='session')body=`<section class="panel"><h2>全部 Sessions</h2>${table('session')}</section>`;else body=`<section class="panel"><h2>数据口径</h2><p class="subtle">这是由输入文件派生的离线 HTML；它不改变 Dashboard 源数据。</p><div class="table-wrap"><table><thead><tr><th>Source</th><th>摘要</th></tr></thead><tbody>${data.source_manifest.map(x=>`<tr><td>${esc(x.path||x.source||x)}</td><td>${esc(x.sha256||x.note||'')}</td></tr>`).join('')}</tbody></table></div></section>`;$('view').innerHTML=body}
readHash();metrics();render();document.addEventListener('click',e=>{const tab=e.target.closest('[data-view]');if(tab){state.view=tab.dataset.view;state.page=1;render();return}const op=e.target.closest('[data-open]');if(op){openDetail(op.dataset.open,op.dataset.id);return}const pg=e.target.closest('[data-page]');if(pg&&!pg.disabled){state.page+=pg.dataset.page==='next'?1:-1;render()}});Object.values(filters).forEach(e=>e.addEventListener(e===filters.q?'input':'change',()=>{state.page=1;render()}));sortSelect.addEventListener('change',()=>{state.page=1;render()});$('reset').addEventListener('click',()=>{Object.values(filters).forEach(e=>e.value='');sortSelect.value='source';state.page=1;render()});$('drawer-close').addEventListener('click',()=>{$('drawer').classList.remove('open');$('drawer').setAttribute('aria-hidden','true')});
</script></body></html>'''


def render(data: dict[str, Any], output: Path) -> None:
    page = HTML_TEMPLATE.replace("__TITLE__", html.escape(text(data.get("title"), "Exploration Dashboard")))
    page = page.replace("__SUBTITLE__", html.escape(text(data.get("subtitle"))))
    page = page.replace("__DATA__", json_script(data))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Dashboard JSON or standard Markdown")
    parser.add_argument("output", type=Path, help="standalone HTML output path")
    args = parser.parse_args()
    render(load_input(args.input), args.output)
    print(f"Rendered {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
