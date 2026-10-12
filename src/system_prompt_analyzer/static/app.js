const form = document.querySelector("#analyze-form");
const promptInput = document.querySelector("#prompt");
const wordCount = document.querySelector("#word-count");
const results = document.querySelector("#results");
const button = document.querySelector("#analyze-button");
const template = document.querySelector("#results-template");

promptInput.addEventListener("input", () => {
  const words = promptInput.value.trim().split(/\s+/).filter(Boolean).length;
  wordCount.textContent = `${words} ${words === 1 ? "word" : "words"}`;
});

function renderResults(data) {
  const fragment = template.content.cloneNode(true);
  fragment.querySelector(".result-summary").textContent = data.summary;
  const map = fragment.querySelector(".map");

  data.nodes.forEach((node, index) => {
    const element = document.createElement("article");
    element.className = `node ${node.id === "prompt" ? "root" : ""} ${node.status}`;
    element.dataset.kind = node.kind;
    element.style.animationDelay = `${Math.min(index * 35, 350)}ms`;
    element.setAttribute("role", "listitem");

    const meta = document.createElement("div");
    meta.className = "node-kind";
    const kind = document.createElement("span");
    kind.textContent = node.kind;
    const status = document.createElement("span");
    status.textContent = node.status;
    meta.append(kind, status);

    const title = document.createElement("h3");
    title.textContent = node.title;
    const detail = document.createElement("p");
    detail.textContent = node.detail;
    element.append(meta, title, detail);
    map.append(element);
  });

  results.replaceChildren(fragment);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  button.querySelector("span:first-child").textContent = "Mapping…";

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: promptInput.value }),
    });
    if (!response.ok) throw new Error("The prompt could not be analyzed.");
    renderResults(await response.json());
  } catch (error) {
    const message = document.createElement("div");
    message.className = "error";
    message.textContent = error.message;
    results.replaceChildren(message);
  } finally {
    button.disabled = false;
    button.querySelector("span:first-child").textContent = "Analyze prompt";
  }
});

fetch("/api/config")
  .then((response) => response.json())
  .then((config) => {
    if (!config.api_key_configured) return;
    const status = document.querySelector("#provider-status");
    status.querySelector(".status-dot").classList.add("connected");
    status.querySelector("span:last-child").textContent = `${config.provider} · ${config.model}`;
  })
  .catch(() => {});
