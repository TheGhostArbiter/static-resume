"""Functional UI tests for the home page FX panel + swipe gestures.

Each test is an async function that takes (chrome, base_url) and returns
(name, ok, message). Run via `python3 tests/test_home.py` from the repo root.
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ChromeSession, serve_directory  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8766
BASE = f"http://localhost:{PORT}"

ATMOSPHERES = [
    "blue", "crimson", "emerald", "violet", "ghost", "void",
    "amethyst", "neon-rose", "chrome", "prism", "castle",
]
GET_ATM = "document.documentElement.getAttribute('data-atmosphere')"


# ─── Page load + structure ──────────────────────────────────────────────

async def test_page_loads_clean(c):
    await c.goto(BASE + "/", clear_storage=True)
    # Ignore the third-party three.js deprecation warning from the CDN bundle.
    real_errors = [e for e in c.errors if "three.js" not in e.lower()]
    return (
        "Page loads with no JS errors",
        not real_errors,
        f"errors={real_errors!r}",
    )


async def test_fx_panel_renders(c):
    await c.goto(BASE + "/")
    exists = await c.eval("!!document.getElementById('fxPanel')")
    count = await c.eval("document.querySelectorAll('.fx-toggle').length")
    keys = await c.eval(
        "Array.from(document.querySelectorAll('.fx-toggle'))"
        ".map(function(i){return i.getAttribute('data-fx');}).join(',')"
    )
    expected_keys = "spotlight,tilt,sparks,swipe,confetti"
    return (
        "FX panel renders with the expected 5 toggles",
        exists and count == 5 and keys == expected_keys,
        f"exists={exists} count={count} keys={keys}",
    )


async def test_subpages_load_without_BSC_FX(c):
    """Sub-pages load shared-enhancements.js but don't define BSC_FX —
    the fxOn helper must default to on so behavior is unchanged.
    """
    failures = []
    for page in (
        "resume-atlas.html",
        "resume-signal.html",
        "proof-hub.html",
        "resume-switchboard.html",
    ):
        await c.goto(f"{BASE}/{page}", clear_storage=True)
        if c.errors:
            failures.append(f"{page}: {c.errors!r}")
        has_fx = await c.eval("!!window.BSC_FX")
        if has_fx:
            failures.append(f"{page}: unexpectedly exposes BSC_FX")
    return (
        "All sub-pages load with no JS errors and don't expose BSC_FX",
        not failures,
        "; ".join(failures) or "4/4 pages OK",
    )


# ─── BSC_FX state + persistence ─────────────────────────────────────────

async def test_fx_defaults(c):
    await c.goto(BASE + "/", clear_storage=True)
    state = json.loads(await c.eval("JSON.stringify(window.BSC_FX.all())"))
    expected = {
        "spotlight": True, "tilt": True, "sparks": True,
        "confetti": True, "swipe": True,
    }
    return (
        "BSC_FX defaults are all-on",
        state == expected,
        f"got {state}",
    )


async def test_fx_set_persists(c):
    await c.goto(BASE + "/", clear_storage=True)
    await c.eval("window.BSC_FX.set('spotlight', false)")
    raw = await c.eval("localStorage.getItem('bsc_fx')")
    parsed = json.loads(raw) if raw else {}
    return (
        "BSC_FX.set persists to localStorage",
        parsed.get("spotlight") is False,
        f"localStorage: {raw}",
    )


async def test_fx_state_survives_reload(c):
    await c.goto(BASE + "/", clear_storage=True)
    await c.eval("window.BSC_FX.set('sparks', false)")
    await c.goto(BASE + "/")  # reload without clearing
    state = json.loads(await c.eval("JSON.stringify(window.BSC_FX.all())"))
    return (
        "BSC_FX state survives page reload",
        state.get("sparks") is False,
        f"after reload: {state}",
    )


async def test_fx_change_event(c):
    await c.goto(BASE + "/", clear_storage=True)
    captured = await c.eval(
        "(function(){"
        "var got = null;"
        "window.addEventListener('bsc-fx-change',"
        "function(ev){got = ev.detail;},{once:true});"
        "window.BSC_FX.set('tilt', false);"
        "return JSON.stringify(got);"
        "})()"
    )
    detail = json.loads(captured) if captured else None
    ok = bool(detail and detail.get("key") == "tilt" and detail.get("value") is False)
    return (
        "bsc-fx-change event fires with {key, value} detail",
        ok,
        f"detail: {detail}",
    )


async def test_checkbox_syncs_with_programmatic_set(c):
    await c.goto(BASE + "/", clear_storage=True)
    await c.eval("window.BSC_FX.set('spotlight', false)")
    checked = await c.eval(
        "document.querySelector('input[data-fx=\"spotlight\"]').checked"
    )
    row_on = await c.eval(
        "document.querySelector('[data-fx-row=\"spotlight\"]').getAttribute('data-on')"
    )
    return (
        "Checkbox + row[data-on] sync when BSC_FX.set is called externally",
        checked is False and row_on == "false",
        f"checked={checked} data-on={row_on}",
    )


async def test_checkbox_click_updates_state(c):
    await c.goto(BASE + "/", clear_storage=True)
    await c.eval(
        "(function(){var i=document.querySelector('input[data-fx=\"confetti\"]');"
        "i.checked=false; i.dispatchEvent(new Event('change',{bubbles:true}));})()"
    )
    state = json.loads(await c.eval("JSON.stringify(window.BSC_FX.all())"))
    raw = await c.eval("localStorage.getItem('bsc_fx')")
    persisted = json.loads(raw) if raw else {}
    return (
        "Toggling a checkbox updates BSC_FX state and persists",
        state.get("confetti") is False and persisted.get("confetti") is False,
        f"runtime={state.get('confetti')} stored={persisted.get('confetti')}",
    )


# ─── Swipe: full cycle + wrap-around in both directions ──────────────────

async def _reset_atm(c, atm="blue"):
    await c.eval(f"document.documentElement.setAttribute('data-atmosphere','{atm}')")
    await c.eval("window.BSC_FX.set('swipe', true)")


async def test_swipe_forward_full_cycle(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    failures = []
    for step in range(len(ATMOSPHERES) + 1):  # +1 to cross the wrap boundary
        before = await c.eval(GET_ATM)
        expected = ATMOSPHERES[(ATMOSPHERES.index(before) + 1) % len(ATMOSPHERES)]
        await c.swipe("left", pid=1000 + step)
        await asyncio.sleep(0.18)
        after = await c.eval(GET_ATM)
        if after != expected:
            failures.append(f"step {step+1}: {before}→{after} expected {expected}")
    return (
        "Forward swipe cycles all 11 atmospheres + wraps castle→blue",
        not failures,
        "; ".join(failures) or f"{len(ATMOSPHERES)+1}/{len(ATMOSPHERES)+1} steps OK",
    )


async def test_swipe_reverse_full_cycle(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    failures = []
    for step in range(len(ATMOSPHERES) + 1):
        before = await c.eval(GET_ATM)
        expected = ATMOSPHERES[(ATMOSPHERES.index(before) - 1) % len(ATMOSPHERES)]
        await c.swipe("right", pid=2000 + step)
        await asyncio.sleep(0.18)
        after = await c.eval(GET_ATM)
        if after != expected:
            failures.append(f"step {step+1}: {before}→{after} expected {expected}")
    return (
        "Reverse swipe cycles all 11 atmospheres + wraps blue→castle",
        not failures,
        "; ".join(failures) or f"{len(ATMOSPHERES)+1}/{len(ATMOSPHERES)+1} steps OK",
    )


# ─── Swipe: threshold + exclusion guards ─────────────────────────────────

async def test_slow_drag_ignored(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    before = await c.eval(GET_ATM)
    await c.slow_drag(dx=-800, pid=3001)
    await asyncio.sleep(0.25)
    after = await c.eval(GET_ATM)
    return (
        "Slow drag (under velocity threshold) does NOT cycle atmosphere",
        before == after,
        f"before={before} after={after}",
    )


async def test_diagonal_swipe_ignored(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    before = await c.eval(GET_ATM)
    # 45° fast drag — should fail the |Δx| ≥ 2.4·|Δy| dominance check.
    await c.eval(
        "(function(){var pid=4001;"
        "var f=function(t,x,y){document.dispatchEvent(new PointerEvent(t,"
        "{pointerType:'touch',clientX:x,clientY:y,button:0,pointerId:pid,"
        "isPrimary:true,bubbles:true}));};"
        "f('pointerdown',900,200);"
        "f('pointermove',600,400);"
        "f('pointermove',300,600);"
        "f('pointerup',100,750);})()"
    )
    await asyncio.sleep(0.2)
    after = await c.eval(GET_ATM)
    return (
        "Diagonal swipe (failing horizontal-dominance) does NOT cycle atmosphere",
        before == after,
        f"before={before} after={after}",
    )


async def test_swipe_on_interactive_target_ignored(c):
    """Swiping that starts on a button/link should NOT cycle atmosphere —
    it would steal clicks from the UI otherwise.
    """
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    before = await c.eval(GET_ATM)
    # Simulate pointerdown on the existing CTA button, then drag away
    started = await c.eval(
        "(function(){var el=document.querySelector('a[data-mode=\"resume-atlas.html\"]');"
        "if(!el) return false;"
        "var r=el.getBoundingClientRect(); var sx=r.left+r.width/2, sy=r.top+r.height/2;"
        "var pid=5050;"
        "var f=function(t,x,y){var ev=new PointerEvent(t,{pointerType:'touch',"
        "clientX:x,clientY:y,button:0,pointerId:pid,isPrimary:true,bubbles:true});"
        "(t==='pointerdown'?el:document).dispatchEvent(ev);};"
        "f('pointerdown',sx,sy);"
        "f('pointermove',sx-300,sy+3);"
        "f('pointermove',sx-600,sy+5);"
        "f('pointerup',sx-800,sy+6);"
        "return true;})()"
    )
    await asyncio.sleep(0.2)
    after = await c.eval(GET_ATM)
    return (
        "Swipe starting on a CTA link does NOT cycle atmosphere",
        bool(started) and before == after,
        f"started={started} before={before} after={after}",
    )


async def test_swipe_disabled_blocks_gesture(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    await c.eval("window.BSC_FX.set('swipe', false)")
    before = await c.eval(GET_ATM)
    await c.swipe("left", pid=6001)
    await asyncio.sleep(0.2)
    after = await c.eval(GET_ATM)
    return (
        "Disabling 'swipe' FX blocks the atmosphere-cycling gesture",
        before == after,
        f"before={before} after={after}",
    )


# ─── Vertical gestures ───────────────────────────────────────────────────

async def test_swipe_up_opens_palette(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    before_open = await c.eval("!document.getElementById('cmd-pal').hidden")
    await c.swipe("up", pid=7001)
    await asyncio.sleep(0.3)
    after_open = await c.eval("!document.getElementById('cmd-pal').hidden")
    return (
        "Swipe up opens the command palette",
        (not before_open) and after_open,
        f"before_open={before_open} after_open={after_open}",
    )


async def test_swipe_down_triggers_confetti(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    await c.eval("window.BSC_FX.set('confetti', true)")
    await c.eval("document.getElementById('confetti').classList.remove('is-on')")
    await c.swipe("down", pid=8001)
    await asyncio.sleep(0.5)
    on = await c.eval(
        "document.getElementById('confetti').classList.contains('is-on')"
    )
    return (
        "Swipe down triggers confetti burst",
        bool(on),
        f"confetti is-on={on}",
    )


async def test_confetti_off_blocks_swipe_down(c):
    await c.goto(BASE + "/", clear_storage=True)
    await _reset_atm(c, "blue")
    await c.eval("window.BSC_FX.set('confetti', false)")
    await c.eval("document.getElementById('confetti').classList.remove('is-on')")
    await c.swipe("down", pid=9001)
    await asyncio.sleep(0.5)
    on = await c.eval(
        "document.getElementById('confetti').classList.contains('is-on')"
    )
    return (
        "Confetti FX off → swipe-down does NOT fire confetti",
        not on,
        f"confetti is-on={on}",
    )


# ─── New: stack footer, ?for= personalization, /now, per-case share ─────

async def test_stack_footer_injected_on_home(c):
    await c.goto(BASE + "/", clear_storage=True)
    await asyncio.sleep(0.15)
    present = await c.eval("!!document.querySelector('[data-bsc-stack]')")
    return (
        "Stack-disclosure line is injected into the footer",
        bool(present),
        f"present={present}",
    )


async def test_stack_footer_present_on_all_entry_points(c):
    pages = (
        "/",
        "resume-atlas.html",
        "resume-signal.html",
        "proof-hub.html",
        "resume-switchboard.html",
        "now.html",
    )
    failures = []
    for page in pages:
        url = BASE + ("/" + page if not page.startswith("/") else page)
        await c.goto(url, clear_storage=True)
        await asyncio.sleep(0.15)
        present = await c.eval("!!document.querySelector('[data-bsc-stack]')")
        if not present:
            failures.append(page)
    return (
        "Stack-disclosure footer present on all 6 entry points",
        not failures,
        "; ".join(failures) or f"{len(pages)}/{len(pages)} pages OK",
    )


async def test_for_param_personalizes(c):
    await c.goto(BASE + "/?for=stripe", clear_storage=True)
    # Give the fetch + DOM injection a moment to settle.
    for _ in range(20):
        present = await c.eval("!!document.querySelector('[data-for-badge]')")
        if present:
            break
        await asyncio.sleep(0.1)
    atm = await c.eval(GET_ATM)
    badge_text = await c.eval(
        "(function(){var b=document.querySelector('[data-for-badge]');"
        "return b ? b.textContent : '';})()"
    )
    return (
        "?for=stripe pins emerald atmosphere AND shows 'Tailored for Stripe' badge",
        atm == "emerald" and "Stripe" in (badge_text or ""),
        f"atmosphere={atm} badge_text={badge_text!r}",
    )


async def test_for_param_unknown_slug_is_silent(c):
    await c.goto(BASE + "/?for=nonexistent-co-99", clear_storage=True)
    await asyncio.sleep(0.3)
    badge = await c.eval("!!document.querySelector('[data-for-badge]')")
    real_errors = [e for e in c.errors if "three.js" not in e.lower()]
    return (
        "Unknown ?for= slug fails silently — no badge, no JS error",
        not badge and not real_errors,
        f"badge={badge} errors={real_errors!r}",
    )


async def test_now_page_loads_with_sections(c):
    await c.goto(BASE + "/now.html", clear_storage=True)
    real_errors = [e for e in c.errors if "three.js" not in e.lower()]
    sections = await c.eval(
        "Array.from(document.querySelectorAll('section.card h2'))"
        ".map(function(h){return h.textContent.trim();}).join('|')"
    )
    expected = ["Currently building", "Currently learning", "Currently reading", "Open to"]
    missing = [s for s in expected if s not in sections]
    return (
        "/now.html loads with all four expected section headings and no JS errors",
        not real_errors and not missing,
        f"errors={real_errors!r} missing={missing} got={sections!r}",
    )


async def test_proof_hub_case_anchors_exist(c):
    await c.goto(BASE + "/proof-hub.html", clear_storage=True)
    ids = await c.eval(
        "Array.from(document.querySelectorAll('[id^=\"case-\"]'))"
        ".map(function(el){return el.id;}).sort().join(',')"
    )
    expected = "case-data-foundations,case-java-etl,case-payment-portal,case-secure-provisioning,case-serverless-bus"
    return (
        "Proof Hub exposes all 5 case anchors (id=case-<slug>)",
        ids == expected,
        f"got: {ids}",
    )


async def test_proof_hub_case_share_buttons_render(c):
    await c.goto(BASE + "/proof-hub.html", clear_storage=True)
    await asyncio.sleep(0.2)
    count = await c.eval("document.querySelectorAll('[data-case-share]').length")
    return (
        "Each case anchor gets a [data-case-share] copy-link button",
        count == 5,
        f"count={count}",
    )


# ─── Runner ──────────────────────────────────────────────────────────────

TESTS = [
    test_page_loads_clean,
    test_fx_panel_renders,
    test_subpages_load_without_BSC_FX,
    test_fx_defaults,
    test_fx_set_persists,
    test_fx_state_survives_reload,
    test_fx_change_event,
    test_checkbox_syncs_with_programmatic_set,
    test_checkbox_click_updates_state,
    test_swipe_forward_full_cycle,
    test_swipe_reverse_full_cycle,
    test_slow_drag_ignored,
    test_diagonal_swipe_ignored,
    test_swipe_on_interactive_target_ignored,
    test_swipe_disabled_blocks_gesture,
    test_swipe_up_opens_palette,
    test_swipe_down_triggers_confetti,
    test_confetti_off_blocks_swipe_down,
    test_stack_footer_injected_on_home,
    test_stack_footer_present_on_all_entry_points,
    test_for_param_personalizes,
    test_for_param_unknown_slug_is_silent,
    test_now_page_loads_with_sections,
    test_proof_hub_case_anchors_exist,
    test_proof_hub_case_share_buttons_render,
]


async def main():
    server = serve_directory(ROOT, port=PORT)
    async with ChromeSession(port=9438) as chrome:
        print(f"Running {len(TESTS)} tests against {BASE}\n")
        results = []
        for fn in TESTS:
            try:
                name, ok, msg = await fn(chrome)
            except Exception as e:
                name, ok, msg = fn.__name__, False, f"EXCEPTION: {e!r}"
            results.append((name, ok, msg))
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}")
            if not ok:
                print(f"         → {msg}")
        passed = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        print(f"\n{passed}/{total} passed")
    server.terminate()
    try:
        server.wait(timeout=3)
    except Exception:
        server.kill()
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    asyncio.run(main())
