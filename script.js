const parseBtn = document.getElementById("parse-btn");
const fileInput = document.getElementById("file-upload");
const loadingEl = document.getElementById("loading");
const resultEl = document.getElementById("result");
const jsonOut = document.getElementById("json-output");
const downloadJson = document.getElementById("download-json");
const downloadCsv = document.getElementById("download-csv");
const darkToggle = document.getElementById("dark-toggle");

// Dark mode persist
if (localStorage.getItem("dark") === "1") {
  document.body.classList.add("dark");
  darkToggle.checked = true;
}
darkToggle?.addEventListener("change", () => {
  if (darkToggle.checked) {
    document.body.classList.add("dark");
    localStorage.setItem("dark", "1");
  } else {
    document.body.classList.remove("dark");
    localStorage.setItem("dark", "0");
  }
});

parseBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    alert("Please choose a resume (.pdf or .docx) first.");
    return;
  }

  // show loading
  loadingEl.classList.remove("hidden");
  resultEl.classList.add("hidden");
  jsonOut.textContent = "";

  try {
    const form = new FormData();
    form.append("resume", file);

    const res = await fetch("http://127.0.0.1:5000/parse", {
      method: "POST",
      body: form
    });

    if (!res.ok) {
      const txt = await res.text();
      alert("Backend error: " + txt);
      throw new Error(txt);
    }

    const payload = await res.json();

    // payload structure: { parsed: {...}, json_filename: "...", csv_filename: "..." }
    const parsed = payload.parsed || payload; // some older parsers returned object directly
    jsonOut.textContent = JSON.stringify(parsed, null, 2);
    resultEl.classList.remove("hidden");

    // Create client-side download links as a fallback
    const jsonBlob = new Blob([JSON.stringify(parsed, null, 2)], { type: "application/json" });
    const jsonUrl = URL.createObjectURL(jsonBlob);
    downloadJson.href = jsonUrl;
    downloadJson.download = payload.json_filename || "parsed.json";

    // CSV fallback: create simple CSV
    const skills = (parsed.skills || []).join("; ");
    const csv = `email,phone,skills,education_count,experience_count\n` +
                `"${parsed.email || ""}","${parsed.phone || ""}","${skills}",${(parsed.education||[]).length},${(parsed.experience||[]).length}`;
    const csvBlob = new Blob([csv], { type: "text/csv" });
    const csvUrl = URL.createObjectURL(csvBlob);
    downloadCsv.href = csvUrl;
    downloadCsv.download = payload.csv_filename || "summary.csv";

    // If backend saved files and provided filenames, override hrefs to backend download endpoints
    if (payload.json_filename) {
      downloadJson.href = `http://127.0.0.1:5000/download/json/${encodeURIComponent(payload.json_filename)}`;
    }
    if (payload.csv_filename) {
      downloadCsv.href = `http://127.0.0.1:5000/download/csv/${encodeURIComponent(payload.csv_filename)}`;
    }

  } catch (err) {
    console.error(err);
    // if fetch or parse errored we already alerted
  } finally {
    loadingEl.classList.add("hidden");
  }
});
