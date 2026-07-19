"""Opportunity Atlas — a dependency-free Python demo for AI use-case portfolios."""

from __future__ import annotations

import json
import os
import random
import re
import urllib.error
import urllib.request
from urllib.parse import unquote
from copy import deepcopy
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from collaboration import Collaboration, FieldLockedError
from ai_suggestions import apply_suggested_weights, suggest_for_iteration
from ranking import default_rubric, validate_rubric
from workspace import CHART_ROOM_FIELD_IDS, Workspace

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
DATA = ROOT / "data" / "portfolio.json"
WORKSPACE_DATA = ROOT / "data" / "workspace.json"

DEFAULT_PORTFOLIO = {
    "workspace": {
        "name": "Northstar Operations AI Portfolio",
        "context": "Northstar supports growing B2B customers. Its teams need to reduce repetitive support work while keeping customer-facing decisions accountable.",
        "goals": "Improve customer response quality, protect specialist time, and make AI investment decisions evidence-led.",
    },
    "dimensions": [
        {"id": "value", "name": "Expected value", "description": "Benefit if this works", "weight": 25, "direction": "higher"},
        {"id": "alignment", "name": "Strategic alignment", "description": "Fit with current priorities", "weight": 20, "direction": "higher"},
        {"id": "readiness", "name": "Data readiness", "description": "Quality and availability of inputs", "weight": 18, "direction": "higher"},
        {"id": "effort", "name": "Delivery effort", "description": "Time and coordination required", "weight": 15, "direction": "lower"},
        {"id": "risk", "name": "Risk", "description": "Potential harm or governance burden", "weight": 12, "direction": "lower"},
        {"id": "confidence", "name": "Evidence confidence", "description": "Strength of the evidence", "weight": 10, "direction": "higher"},
    ],
    "use_cases": [
        {"id": "ticket-triage", "title": "Support ticket signal triage", "stage": "shaped", "user": "Support operations lead", "workflow": "Inbound support", "summary": "Group repeated issues and draft incident signals from incoming tickets.", "current": "Leads scan hundreds of tickets manually and detect repeats late.", "ai_state": "AI clusters tickets and drafts an incident brief; a lead reviews before escalation.", "outcome": "Faster incident detection without automating customer decisions.", "evidence": "Two weekly incident reviews and 1,800 tickets per month.", "assessments": {"value": [5, "High volume and delayed detection create clear cost."], "alignment": [5, "Directly supports response quality."], "readiness": [4, "Ticket metadata and text are available."], "effort": [3, "Needs help-desk integration."], "risk": [2, "Human reviews every escalation."], "confidence": [4, "Volume and workflow are known."]}},
        {"id": "renewal-brief", "title": "Renewal preparation brief", "stage": "shortlisted", "user": "Customer success manager", "workflow": "Account renewal", "summary": "Prepare an evidence-led account brief before renewal calls.", "current": "Managers compile product usage, tickets, and notes across tools.", "ai_state": "AI drafts a brief with citations for a manager to verify.", "outcome": "More consistent preparation and fewer missed account risks.", "evidence": "Managers report 45–60 minutes of preparation per strategic account.", "assessments": {"value": [4, "Saves meaningful senior time."], "alignment": [4, "Supports retention."], "readiness": [3, "Data is spread across systems."], "effort": [4, "Several integrations are required."], "risk": [3, "Incorrect summaries can affect a relationship."], "confidence": [3, "Time estimate is self-reported."]}},
        {"id": "knowledge-gaps", "title": "Knowledge-base gap finder", "stage": "discovered", "user": "Knowledge manager", "workflow": "Help-center maintenance", "summary": "Identify unanswered recurring questions and candidate article gaps.", "current": "Article updates follow anecdotal reports and quarterly reviews.", "ai_state": "AI highlights repeated unresolved intents for editorial review.", "outcome": "A more relevant help centre and fewer repeat contacts.", "evidence": "Support tags exist, but intent data is inconsistent.", "assessments": {"value": [4, "Potential deflection benefit."], "alignment": [3, "Useful but indirect."], "readiness": [3, "Ticket data exists but needs cleanup."], "effort": [2, "Can start with exports."], "risk": [2, "Editors approve output."], "confidence": [3, "Need baseline deflection data."]}},
        {"id": "qa-coach", "title": "Support quality coaching", "stage": "discovered", "user": "Support team lead", "workflow": "Quality assurance", "summary": "Surface coaching moments from customer conversations.", "current": "Leads sample a small share of conversations manually.", "ai_state": "AI flags potential coaching moments for lead review.", "outcome": "Broader feedback coverage while retaining manager judgement.", "evidence": "Existing QA rubric and anonymised ticket transcripts.", "assessments": {"value": [4, "Improves quality at team scale."], "alignment": [4, "Matches service-quality goal."], "readiness": [4, "Rubric and transcripts exist."], "effort": [3, "Requires rubric calibration."], "risk": [4, "Could be misused for employee performance."], "confidence": [3, "Impact hypothesis needs validation."]}},
        {"id": "onboarding-guide", "title": "Implementation onboarding guide", "stage": "not pursuing", "user": "Implementation consultant", "workflow": "Customer onboarding", "summary": "Draft account-specific onboarding plans from discovery notes.", "current": "Consultants create plans manually from call notes.", "ai_state": "AI drafts a plan for consultant review.", "outcome": "Faster first draft of a customer plan.", "evidence": "Templates are inconsistent across consultants.", "assessments": {"value": [3, "Useful time saving."], "alignment": [3, "Not a current priority."], "readiness": [2, "Notes vary substantially."], "effort": [3, "Needs template work."], "risk": [3, "Bad plan can set expectations."], "confidence": [2, "No volume baseline."]}},
        {"id": "voice-of-customer", "title": "Voice of customer themes", "stage": "discovered", "user": "Product manager", "workflow": "Product discovery", "summary": "Synthesize recurring customer needs from support and interview feedback.", "current": "Insights are collected manually and arrive too late for planning.", "ai_state": "AI proposes traceable themes with source excerpts for product review.", "outcome": "Faster, more evidence-linked product discovery.", "evidence": "Interview notes and support data are available.", "assessments": {"value": [5, "Influences roadmap choices."], "alignment": [4, "Supports customer-led growth."], "readiness": [3, "Sources need a common format."], "effort": [3, "Moderate ingestion and review workflow."], "risk": [3, "Sampling bias needs visibility."], "confidence": [3, "Need validate with product team."]}},
    ],
    "decision": {"selected_id": "ticket-triage", "rationale": "Prioritize support ticket signal triage: it combines a high-volume pain with available data and a clear human review point."},
}

def _seeded_workspace() -> Workspace:
    """Build the open first Opportunity Map shown on a fresh Workspace."""
    return Workspace.start(
        ai_vision="AI should make specialists faster and more confident without ever making a customer-facing decision unaccountable.",
        ai_strategy="This quarter: reduce repetitive support work and strengthen the evidence behind renewal and onboarding decisions, while keeping every AI-assisted step reviewable by a person.",
        map_focus="Find AI-assisted ways to improve customer response quality while protecting specialist time.",
        opportunities=[
            {
                "id": "ticket-triage",
                "title": "Support ticket signal triage",
                "summary": "Spot repeated customer issues before they become incidents.",
                "evaluation": {
                    "value": {"score": 5, "rationale": "High ticket volume makes delayed patterns costly."},
                    "readiness": {"score": 4, "rationale": "Ticket text and metadata are already available."},
                    "effort": {"score": 3, "rationale": "A help-desk integration is needed."},
                },
            },
            {
                "id": "renewal-brief",
                "title": "Renewal preparation brief",
                "summary": "Help account teams prepare for strategic renewal conversations.",
                "evaluation": {
                    "value": {"score": 4, "rationale": "Preparation currently takes senior time."},
                    "readiness": {"score": 3, "rationale": "Useful context is spread across systems."},
                    "effort": {"score": 4, "rationale": "Several sources must be connected."},
                },
            },
            {
                "id": "knowledge-gaps",
                "title": "Knowledge-base gap finder",
                "summary": "Find unanswered customer questions worth turning into help content.",
                "evaluation": {
                    "value": {"score": 4, "rationale": "Better self-service could prevent repeat contacts."},
                    "readiness": {"score": 3, "rationale": "Support tags exist, but intent data needs cleanup."},
                    "effort": {"score": 2, "rationale": "The team can start with a small export."},
                },
            },
        ],
        dimensions=[],
        assessments={},
        custom_name="Customer Support",
    )


DEFAULT_WORKSPACE = _seeded_workspace()

COLLABORATION = Collaboration()


def load_portfolio():
    if not DATA.exists():
        DATA.parent.mkdir(parents=True, exist_ok=True)
        save_portfolio(deepcopy(DEFAULT_PORTFOLIO))
    return json.loads(DATA.read_text(encoding="utf-8"))


def save_portfolio(portfolio):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(portfolio, indent=2), encoding="utf-8")


def load_workspace():
    if not WORKSPACE_DATA.exists():
        save_workspace(DEFAULT_WORKSPACE)
    return Workspace.from_dict(json.loads(WORKSPACE_DATA.read_text(encoding="utf-8")))


def save_workspace(workspace):
    WORKSPACE_DATA.parent.mkdir(parents=True, exist_ok=True)
    WORKSPACE_DATA.write_text(json.dumps(workspace.to_dict(), indent=2), encoding="utf-8")


def workspace_payload(workspace: Workspace) -> dict:
    """Expose the editable Workspace and its Map metadata."""
    payload = workspace.to_dict()
    current = workspace.current_iteration
    payload["ranking"] = workspace.current_ranking() if current.dimensions else []
    payload["map"] = {
        "name": current.name,
        "focus": current.map_focus,
        "is_editable": current.is_editable,
    }
    payload["north_star"] = {
        "ai_vision": workspace.ai_vision,
        "ai_strategy": workspace.ai_strategy,
        "ai_vision_missing": not bool(workspace.ai_vision),
        "ai_strategy_missing": not bool(workspace.ai_strategy),
    }
    payload["expedition"] = workspace.current_expedition
    if payload["expedition"] is not None:
        payload["map_changes"] = {
            "expedition_id": payload["expedition"]["id"],
            **workspace.map_changes_for_expedition(payload["expedition"]["id"]),
        }
    return payload


def apply_auto_save(workspace: Workspace, field_id: str, value: object) -> None:
    """Persist a supported draft field after Collaboration's debounce elapses."""
    current = workspace.current_iteration
    if not current.is_editable:
        raise ValueError("A set Iteration cannot be changed.")
    if field_id == "decision-frame.goal":
        if not isinstance(value, str) or not value.strip():
            raise ValueError("The Decision Frame goal cannot be empty.")
        current.map_focus = value.strip()
        return
    raise ValueError(f"Unknown editable field '{field_id}'.")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def clean_portfolio(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("dimensions"), list) or not isinstance(payload.get("use_cases"), list):
        raise ValueError("Portfolio must include dimensions and use_cases.")
    for dimension in payload["dimensions"]:
        dimension["weight"] = max(0, min(100, int(dimension.get("weight", 0))))
        dimension["direction"] = "lower" if dimension.get("direction") == "lower" else "higher"
    return payload


def local_assist(use_case):
    title = use_case.get("title", "This opportunity")
    missing = []
    for field, label in (("current", "the current workflow/pain"), ("ai_state", "the proposed AI-enabled workflow"), ("outcome", "a measurable expected outcome"), ("evidence", "supporting evidence")):
        if not use_case.get(field, "").strip():
            missing.append(label)
    prompt = "Ask the facilitator to add " + ", ".join(missing) + "." if missing else "The core fields are present; make the outcome measurable and verify the evidence source."
    return {"source": "local", "rewrite": f"{title}: help {use_case.get('user') or 'the target user'} improve {use_case.get('workflow') or 'this workflow'} with an AI-assisted step that remains reviewable by a human.", "gaps": prompt}


def openai_assist(use_case, workspace):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return local_assist(use_case)
    instructions = "You improve an AI use-case portfolio entry. Return exactly two short paragraphs labelled REWRITE: and GAPS:. Do not make strategic decisions or invent facts."
    body = json.dumps({"model": "gpt-5.6", "instructions": instructions, "input": json.dumps({"workspace_context": workspace, "use_case": use_case})}).encode()
    request = urllib.request.Request("https://api.openai.com/v1/responses", data=body, method="POST", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read())
        text = "\n".join(item.get("text", "") for output in result.get("output", []) for item in output.get("content", []) if item.get("type") == "output_text")
        rewrite = re.search(r"REWRITE:\s*(.*?)(?=\nGAPS:|$)", text, re.S)
        gaps = re.search(r"GAPS:\s*(.*)$", text, re.S)
        return {"source": "gpt-5.6", "rewrite": rewrite.group(1).strip() if rewrite else text.strip(), "gaps": gaps.group(1).strip() if gaps else "Review the proposed wording with the group."}
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as error:
        fallback = local_assist(use_case)
        fallback["gaps"] += f" (The API was unavailable: {error}.)"
        return fallback


CHART_ROOM_PITFALLS = (
    "Prefer knowledge-synthesis tasks (drafting, summarizing, triage, flagging) over "
    "judgment-heavy tasks (negotiation, hiring, strategy) for a first AI use case.",
    "Measure a baseline before starting; without one you can't prove impact later.",
    "Name one accountable owner; 'the team owns it' reliably predicts failure.",
    "Redesign the workflow around AI; handing out a tool with no process change "
    "produces no real impact.",
    "Define kill/continue criteria up front to avoid pilot purgatory.",
    "Concentrate depth on one process rather than spreading shallowly across many.",
)

EMPTY_ISLAND_CHALLENGE_LINES = (
    "This Island is a blank map. Even I can't challenge nothing — write a sentence "
    "about what's broken today, then I'll have opinions.",
    "There's nothing here yet for me to disagree with. Give me a workflow, a change, "
    "or an outcome, and I'll get to work.",
    "It's Chart Room, but it's an empty Chart Room. Add a line about today's problem "
    "and I'll come back swinging.",
    "An Island this quiet makes a poor sparring partner. Tell me what's supposed to "
    "change, and I'll tell you what worries me.",
    "I can't find a hypothesis to challenge here — only a title. Sketch the workflow "
    "or the outcome first.",
    "Nothing ventured, nothing challenged. Write one honest sentence about the "
    "problem, and I'll push back properly.",
)


def _chart_room_has_content(chart_room):
    """True if any Chart Room field carries non-whitespace text."""
    return any(isinstance(value, str) and value.strip() for value in (chart_room or {}).values())


def local_empty_island_challenge():
    """A trivial, non-network response for an Island with nothing yet to challenge."""
    return {"source": "local", "empty": True, "message": random.choice(EMPTY_ISLAND_CHALLENGE_LINES)}


def _challenge_instructions():
    pitfalls = "\n".join(f"- {pitfall}" for pitfall in CHART_ROOM_PITFALLS)
    return (
        "You challenge one Island in an AI-opportunity Map's Chart Room. Use only the "
        "Chart Room content, evaluation values, and Workspace North Star provided in "
        "the input JSON. Never invent facts, evidence, or numbers not present there. "
        "Frame everything as questions or observations, never as instructions, "
        "rewrites, or decisions — you cannot change Island values, select Islands, "
        "confirm an Expedition, or archive an Island. Consider these pitfalls when "
        f"useful:\n{pitfalls}\n\n"
        "Return exactly three labelled sections, each a short bulleted list ('- ' "
        "prefix, one idea per line):\nMISSING:\nCHALLENGE:\nPITFALL:"
    )


def _parse_challenge_response(text):
    def bullets(match):
        if not match:
            return []
        return [
            re.sub(r"^[-•]\s*", "", line).strip()
            for line in match.group(1).strip().splitlines()
            if line.strip()
        ]

    missing = re.search(r"MISSING:\s*(.*?)(?=\nCHALLENGE:|$)", text, re.S)
    challenge = re.search(r"CHALLENGE:\s*(.*?)(?=\nPITFALL:|$)", text, re.S)
    pitfall = re.search(r"PITFALL:\s*(.*)$", text, re.S)
    return {
        "missing_or_thin": bullets(missing),
        "worth_challenging": bullets(challenge),
        "common_pitfall": bullets(pitfall),
    }


def openai_challenge_island(chart_room, evaluation, north_star):
    """Real GPT-5.6 challenge on team-authored Chart Room content.

    Deliberately has NO local/offline fallback: unlike ``openai_assist``, a
    missing key or a failed call must surface as a plain error, never as
    invented local content standing in for AI's actual read of the Island.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("AI review is unavailable right now.")
    body = json.dumps({
        "model": "gpt-5.6",
        "instructions": _challenge_instructions(),
        "input": json.dumps({"chart_room": chart_room, "evaluation": evaluation, "north_star": north_star}),
    }).encode()
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=body, method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read())
        text = "\n".join(
            item.get("text", "")
            for output in result.get("output", [])
            for item in output.get("content", [])
            if item.get("type") == "output_text"
        )
        return {"source": "gpt-5.6", **_parse_challenge_response(text)}
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError):
        raise ValueError("AI review is unavailable right now.")


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def send_json(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path in {"/", "/index.html"}:
            self.path = "/iteration.html"
        if self.path == "/api/portfolio":
            return self.send_json(HTTPStatus.OK, load_portfolio())
        if self.path == "/api/workspace":
            return self.send_json(HTTPStatus.OK, workspace_payload(load_workspace()))
        return super().do_GET()

    def do_POST(self):
        try:
            payload = self.read_json()
            if self.path == "/api/portfolio":
                portfolio = clean_portfolio(payload)
                save_portfolio(portfolio)
                return self.send_json(HTTPStatus.OK, portfolio)
            if self.path == "/api/workspace/decision":
                workspace = load_workspace()
                iteration = workspace.set_current_iteration(
                    next_opportunity_id=payload["next_opportunity_id"],
                    rationale=payload["rationale"],
                    recorded_by=payload["recorded_by"],
                    unranked_override_rationale=payload.get("unranked_override_rationale"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, {"iteration": iteration.__dict__})
            if self.path == "/api/workspace/next-iteration":
                workspace = load_workspace()
                workspace.start_next_iteration(
                    what_changed=payload["what_changed"],
                    custom_name=payload.get("custom_name"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.CREATED, workspace_payload(workspace))
            if self.path == "/api/workspace/rubric":
                workspace = load_workspace()
                if not workspace.current_iteration.is_editable:
                    raise ValueError("A set Iteration cannot be changed.")
                dimensions = payload["dimensions"]
                validate_rubric(dimensions)
                workspace.current_iteration.dimensions = dimensions
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, workspace_payload(workspace))
            if self.path == "/api/workspace/map":
                workspace = load_workspace()
                workspace.update_current_map(
                    map_focus=payload.get("focus"),
                    name=payload.get("name"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, workspace_payload(workspace))
            if self.path == "/api/workspace/north-star":
                workspace = load_workspace()
                workspace.update_north_star(
                    ai_vision=payload.get("ai_vision"),
                    ai_strategy=payload.get("ai_strategy"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, workspace_payload(workspace))
            if self.path == "/api/ai/suggestions":
                return self.send_json(HTTPStatus.OK, suggest_for_iteration(load_workspace().current_iteration))
            if self.path == "/api/ai/challenge-island":
                workspace = load_workspace()
                chart_room = {
                    field_id: value
                    for field_id, value in (payload.get("chart_room") or {}).items()
                    if field_id in CHART_ROOM_FIELD_IDS
                }
                evaluation = payload.get("evaluation") or {}
                if not isinstance(evaluation, dict):
                    raise ValueError("Island evaluation values must be an object.")
                if not _chart_room_has_content(chart_room):
                    return self.send_json(HTTPStatus.OK, local_empty_island_challenge())
                result = openai_challenge_island(chart_room, evaluation, workspace._north_star_context())
                return self.send_json(HTTPStatus.OK, result)
            if self.path == "/api/workspace/opportunities":
                workspace = load_workspace()
                opportunity = workspace.add_opportunity(payload["opportunity"])
                save_workspace(workspace)
                return self.send_json(HTTPStatus.CREATED, {"opportunity": opportunity})
            if self.path == "/api/workspace/scouting-notes":
                workspace = load_workspace()
                note = workspace.add_scouting_note(
                    title=payload.get("title"),
                    body=payload.get("body"),
                    author=payload.get("author"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.CREATED, {"scouting_note": note})
            if self.path == "/api/workspace/scouting-notes/transfer":
                workspace = load_workspace()
                island = workspace.transfer_scouting_note(
                    note_id=payload.get("note_id"),
                    island_title=payload.get("island_title"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.CREATED, {"opportunity": island})
            if self.path == "/api/workspace/expeditions":
                workspace = load_workspace()
                expedition = workspace.confirm_expedition(
                    charters=payload.get("charters"),
                    planning_horizon=payload.get("planning_horizon", "Current planning cycle"),
                    lens_weights=payload.get("lens_weights"),
                    focus_order=payload.get("focus_order"),
                    override_reason=payload.get("override_reason", ""),
                )
                save_workspace(workspace)
                return self.send_json(
                    HTTPStatus.CREATED,
                    {"expedition": expedition, **workspace_payload(workspace)},
                )
            if self.path.startswith("/api/workspace/opportunities/"):
                opportunity_id = unquote(self.path.rsplit("/", 1)[-1])
                workspace = load_workspace()
                opportunity = workspace.update_opportunity(
                    opportunity_id,
                    title=payload.get("title"),
                    detail=payload.get("detail"),
                    next_move=payload.get("next_move"),
                    ai_formulation=payload.get("ai_formulation"),
                    evaluation=payload.get("evaluation"),
                    chart_room=payload.get("chart_room"),
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, {"opportunity": opportunity})
            if self.path == "/api/workspace/apply-suggested-weights":
                workspace = load_workspace()
                apply_suggested_weights(workspace.current_iteration, payload["weights"])
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, workspace_payload(workspace))
            if self.path == "/api/workspace/archive":
                workspace = load_workspace()
                archive = workspace.archive_inherited_opportunity(
                    opportunity_id=payload["opportunity_id"],
                    reason=payload["reason"],
                )
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, {"archive": archive, **workspace_payload(workspace)})
            if self.path == "/api/workspace/restore":
                workspace = load_workspace()
                opportunity = workspace.restore_inherited_opportunity(payload["opportunity_id"])
                save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, {"opportunity": opportunity, **workspace_payload(workspace)})
            if self.path == "/api/collaboration/start-editing":
                lock = COLLABORATION.start_editing(
                    payload["field_id"], payload["display_name"], at=_now()
                )
                return self.send_json(HTTPStatus.OK, {"field_id": lock.field_id, "holder": lock.holder})
            if self.path == "/api/collaboration/input":
                lock = COLLABORATION.record_input(
                    payload["field_id"], payload["display_name"], payload.get("value"), at=_now()
                )
                return self.send_json(HTTPStatus.ACCEPTED, {"field_id": lock.field_id, "holder": lock.holder})
            if self.path == "/api/collaboration/autosave":
                workspace = load_workspace()
                saves = COLLABORATION.due_auto_saves(at=_now())
                for save in saves:
                    apply_auto_save(workspace, save.field_id, save.value)
                if saves:
                    save_workspace(workspace)
                return self.send_json(HTTPStatus.OK, {"saved_fields": [save.field_id for save in saves]})
            if self.path == "/api/assist":
                portfolio = load_portfolio()
                use_case = next((item for item in portfolio["use_cases"] if item["id"] == payload.get("id")), None)
                if not use_case:
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "Use case not found."})
                return self.send_json(HTTPStatus.OK, openai_assist(use_case, portfolio["workspace"]))
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "Not found."})
        except (ValueError, json.JSONDecodeError) as error:
            return self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Opportunity Atlas running at http://localhost:{port}")
    ThreadingHTTPServer(("", port), AppHandler).serve_forever()
