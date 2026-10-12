from fastapi.testclient import TestClient

from system_prompt_analyzer.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_serves_analyzer() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "System Prompt Analyzer" in response.text
    assert "Analyze prompt" in response.text


def test_analyze_returns_prompt_map() -> None:
    response = client.post(
        "/api/analyze",
        json={"prompt": "Use the browser tool to research the topic."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["analysis_version"] == "1.0.0"
    assert body["rubric_version"] == "1.0.0"
    assert body["nodes"][0]["id"] == "prompt"
    assert any(node["kind"] == "tool" for node in body["nodes"])
    assert any(finding["rule_id"] == "TOOL-001" for finding in body["findings"])
    assert any(node["rule_id"] == "TOOL-001" for node in body["nodes"])


def test_tool_criteria_is_not_suggested_when_present() -> None:
    response = client.post(
        "/api/analyze",
        json={"prompt": "Use the browser tool only when current information is required."},
    )

    assert response.status_code == 200
    finding = next(
        finding
        for finding in response.json()["findings"]
        if finding["rule_id"] == "TOOL-001"
    )
    assert finding["status"] == "present"
    assert finding["evidence"][0]["start_line"] == 1


def test_empty_prompt_is_rejected() -> None:
    response = client.post("/api/analyze", json={"prompt": ""})

    assert response.status_code == 422


def test_rubric_endpoint_exposes_versioned_rules() -> None:
    response = client.get("/api/rubric")

    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.0.0"
    assert body["rules"][0]["id"] == "ROLE-001"
    assert {rule["id"] for rule in body["rules"]} >= {"TOOL-001", "SAFETY-001"}
