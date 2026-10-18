/* The narration booth.
 *
 * One line at a time. The countdown ends, the animation starts and the
 * recorder starts together, so the read is paced by the picture rather than
 * by a stopwatch. The band under the line shows the two numbers that matter:
 * the animation's own length (reading faster than it buys nothing) and the
 * plan's budget for the line (reading past it makes the video longer).
 *
 * Every version of the video is served at once; the picker in the top left
 * switches between them. The version is part of every API path, so a take can
 * only ever land in the audio/ of the cut it was read against.
 */

const $ = (id) => document.getElementById(id);

const el = {
  project: $("project"),
  counts: $("counts"), banner: $("banner"), device: $("device"), meter: $("meter"),
  clip: $("clip"), countdown: $("countdown"), recdot: $("recdot"),
  prev: $("prevline"), line: $("line"), next: $("nextline"),
  band: $("band"), green: $("bandgreen"), mark: $("bandmark"),
  ticks: $("bandticks"), note: $("bandnote"),
  record: $("record"), playclip: $("playclip"), hear: $("hear"),
  keep: $("keep"), redo: $("redo"), undo: $("undo"),
  status: $("status"), list: $("list"),
};

const COUNT_FROM = 3;          // the 3-2-1 before the picture starts
const PAD = 0.35;              // narrate.py's default breathing room

let project = null;            // the version being recorded, from /api/projects
let state = null;              // the whole script, from /api/state/<version>
let beats = [];                // every spoken beat, flat, in order
let current = null;            // the beat being worked on
let stream = null, recorder = null, chunks = [];
let audioCtx = null, analyser = null, meterRaf = null;
let takeBlob = null, takeUrl = null, takeStart = 0, bandRaf = null;
let clipStopper = null, review = null, reviewSource = null;
let busy = false;

// --- talking to the server --------------------------------------------------

/* Which versions there are, and which one to open on. A ?project= in the URL
   wins, so a tab can be left open on one cut while another is recorded in a
   second tab; otherwise the server decides (Professional, unless it has not
   been built yet). */
async function loadProjects() {
  const res = await fetch("/api/projects");
  if (!res.ok) throw new Error(`could not list the versions: ${res.status}`);
  const body = await res.json();

  el.project.replaceChildren();
  for (const p of body.projects) {
    const opt = document.createElement("option");
    opt.value = p.key;
    opt.textContent = p.ready ? p.label : `${p.label} (not built yet)`;
    el.project.append(opt);
  }

  const asked = new URLSearchParams(location.search).get("project");
  const keys = body.projects.map((p) => p.key);
  const key = keys.includes(asked) ? asked : (body.default || keys[0]);
  el.project.value = key;
  project = body.projects.find((p) => p.key === key) || null;
  return key;
}

async function load(selectStem) {
  const res = await fetch(`/api/state/${el.project.value}`);
  if (!res.ok) {
    setStatus(`could not read the script: ${res.status}`, "err");
    return;
  }
  state = await res.json();
  project = state.project;
  beats = state.scenes.flatMap((s) =>
    s.beats.filter((b) => b.spoken).map((b) => ({ ...b, video: s.video })));

  const c = state.counts;
  el.counts.innerHTML =
    `<b>${c.recorded}</b> recorded · ${c.scratch} scratch · ${c.missing} to do ` +
    `<span style="opacity:.6">of ${c.spoken}</span>`;

  if (!project.ready) {
    el.banner.hidden = false;
    el.banner.textContent =
      `${project.detail} — there is nothing to record for ${project.label} ` +
      `until its scenes.py exists. Pick another version above.`;
  } else if (state.needsRender.length) {
    el.banner.hidden = false;
    el.banner.textContent =
      `No current render for ${state.needsRender.join(", ")} — run ` +
      `${project.name}/render.sh so the booth can show you the animation for ` +
      `those lines.`;
  } else {
    el.banner.hidden = true;
  }

  renderList();
  if (!beats.length) {
    current = null;
    el.line.textContent = project.ready
      ? "No narrated beats in this version yet."
      : `${project.label} has not been built yet.`;
    el.prev.textContent = el.next.textContent = "";
    el.note.innerHTML = "";
    el.green.style.width = "0%";
    el.mark.style.left = "0%";
    el.ticks.replaceChildren();
    el.clip.removeAttribute("src");
    el.clip.load();
    for (const b of [el.record, el.hear, el.keep, el.redo, el.undo, el.playclip]) {
      b.disabled = true;
    }
    setStatus("");
    return;
  }
  el.record.disabled = el.playclip.disabled = el.undo.disabled = false;

  const want = selectStem || (current && current.stem) || firstToDo();
  if (want) select(want, { keepTake: selectStem === (current && current.stem) });
}

/* Switching version is a reload of the page's whole world: a take in hand
   belongs to the line it was read against, and carrying it across would be a
   way to save it under the wrong cut. */
async function switchProject(key) {
  if (takeBlob && !confirm("Discard the take you have not kept yet?")) {
    el.project.value = project.key;
    return;
  }
  stopEverything();
  discardTake();
  current = null;
  el.project.value = key;
  const url = new URL(location.href);
  url.searchParams.set("project", key);
  history.replaceState(null, "", url);
  await load();
}

function firstToDo() {
  const todo = beats.find((b) => b.status !== "recorded");
  return (todo || beats[0] || {}).stem;
}

// --- the list ---------------------------------------------------------------

function renderList() {
  el.list.replaceChildren();
  for (const scene of state.scenes) {
    const h = document.createElement("h2");
    h.textContent = scene.name;
    el.list.append(h);
    for (const beat of scene.beats) {
      const row = document.createElement("div");
      row.className = "row" + (beat.spoken ? "" : " silent");
      if (current && beat.stem === current.stem && beat.spoken) {
        row.classList.add("current");
      }
      const dot = document.createElement("span");
      dot.className = "dot " + (beat.spoken ? beat.status : "");
      const text = document.createElement("span");
      text.className = "row-text";
      text.textContent = beat.spoken ? beat.line : beat.line + " (no speech)";
      const dur = document.createElement("span");
      dur.className = "row-dur";
      if (beat.spoken && beat.speech != null) {
        dur.textContent = beat.speech.toFixed(1) + "s";
        if (outsideBand(beat)) dur.classList.add("warn");
      }
      row.append(dot, text, dur);
      if (beat.spoken) row.onclick = () => select(beat.stem);
      el.list.append(row);
    }
  }
}

function outsideBand(beat) {
  if (beat.speech == null) return false;
  const { low, high } = band(beat);
  return beat.speech + PAD < low - GRACE || beat.speech + PAD > high + GRACE;
}

/* The green band: from what the animation costs to what the plan allowed.
   Below the floor the window cannot shrink any further, so the extra speed is
   spent on silence. Above the budget the scene simply gets longer.

   Both numbers are reported as they are. A band can legitimately be narrow —
   some lines really are tightly budgeted — and widening it on screen to look
   comfortable would just be telling the reader something untrue. */
function band(beat) {
  const floor = beat.floor;
  const budget = beat.budget;
  if (floor == null && budget == null) return { low: 0.5, high: 2 };
  if (floor == null) return { low: budget * 0.7, high: budget };
  if (budget == null) return { low: floor, high: floor * 1.3 };
  return { low: floor, high: Math.max(budget, floor) };
}

// How far past the budget still counts as on target. A tenth of a second
// either way is not something anyone can read to.
const GRACE = 0.25;

// --- picking a line ---------------------------------------------------------

function select(stem, opts = {}) {
  if (busy) return;
  const beat = beats.find((b) => b.stem === stem);
  if (!beat) return;
  stopEverything();
  current = beat;
  if (!opts.keepTake) discardTake();

  const i = beats.indexOf(beat);
  el.prev.textContent = i > 0 ? "… " + beats[i - 1].line : "";
  el.next.textContent = i < beats.length - 1 ? beats[i + 1].line + " …" : "";
  el.line.textContent = beat.line;

  drawBand(beat);
  renderList();

  if (beat.video && beat.clipStart != null) {
    // Consecutive beats share a scene, and reloading the same file for each
    // one would re-fetch and re-decode it 46 times over. Only seek.
    if (el.clip.getAttribute("src") !== beat.video) {
      el.clip.setAttribute("src", beat.video);
      el.clip.load();
      el.clip.addEventListener("loadedmetadata", () => {
        el.clip.currentTime = beat.clipStart;
      }, { once: true });
    } else if (el.clip.readyState >= 1) {
      el.clip.currentTime = beat.clipStart;
    }
  } else {
    el.clip.removeAttribute("src");
    el.clip.load();
  }

  el.hear.disabled = beat.status === "missing";
  el.keep.disabled = true;
  el.redo.disabled = true;
  const scratchNote = beat.status === "scratch"
    ? " — currently a scratch take, listen with “Hear it” for the pacing"
    : beat.status === "recorded" ? " — already recorded" : "";
  setStatus(`${beat.scene} beat ${beat.index}${scratchNote}`);
  describeBand(beat, beat.speech);
}

// --- the band ---------------------------------------------------------------

function drawBand(beat, elapsed) {
  const { low, high } = band(beat);
  const scale = Math.max(high * 1.6, (elapsed || 0) * 1.1, 2);
  const pct = (t) => Math.min(100, (t / scale) * 100);
  el.green.style.left = pct(low) + "%";
  // A hairline band would be invisible; 2% is the smallest that still reads.
  el.green.style.width = Math.max(2, pct(high) - pct(low)) + "%";

  // One label only, on the budget. The floor is the band's left edge and
  // needs no number of its own — two labels collide whenever a band is tight.
  el.ticks.replaceChildren();
  const tick = document.createElement("span");
  tick.style.left = pct(high) + "%";
  tick.textContent = high.toFixed(1) + "s";
  el.ticks.append(tick);

  el.mark.style.left = pct(elapsed || 0) + "%";
  el.mark.classList.toggle("over", (elapsed || 0) > high + GRACE);
}

function describeBand(beat, measured) {
  const { low, high } = band(beat);
  const target = `aim for <span class="good">${low.toFixed(1)}–${high.toFixed(1)}s</span>`;
  const why = beat.floor != null && beat.budget != null
    ? ` (the animation runs ${beat.floor.toFixed(1)}s; the plan allowed ` +
      `${beat.budget.toFixed(1)}s)`
    : "";
  if (measured == null) {
    el.note.innerHTML = target + why;
    return;
  }
  const withPad = measured + PAD;
  let verdict;
  if (withPad < low - GRACE) {
    verdict = `<span class="warn">${measured.toFixed(2)}s — quicker than the ` +
      `animation, so there will be a pause after it</span>`;
  } else if (withPad > high + GRACE) {
    verdict = `<span class="warn">${measured.toFixed(2)}s — ` +
      `${(withPad - high).toFixed(1)}s past the plan's budget, which makes ` +
      `the video that much longer</span>`;
  } else {
    verdict = `<span class="good">${measured.toFixed(2)}s — on target</span>`;
  }
  el.note.innerHTML = verdict + " · " + target + why;
}

// --- microphone -------------------------------------------------------------

async function openMic(deviceId) {
  stopMeter();
  if (stream) stream.getTracks().forEach((t) => t.stop());
  const constraints = {
    audio: {
      deviceId: deviceId ? { exact: deviceId } : undefined,
      echoCancellation: false,     // this is narration, not a phone call:
      noiseSuppression: false,     // these would chew the ends off words
      autoGainControl: false,      // and move the level between takes
      channelCount: 1,
    },
  };
  stream = await navigator.mediaDevices.getUserMedia(constraints);
  startMeter();
  return stream;
}

async function listDevices(preferred) {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const mics = devices.filter((d) => d.kind === "audioinput");
  el.device.replaceChildren();
  for (const mic of mics) {
    const opt = document.createElement("option");
    opt.value = mic.deviceId;
    opt.textContent = mic.label || "Microphone";
    el.device.append(opt);
  }
  const saved = preferred || localStorage.getItem("booth.device");
  if (saved && mics.some((m) => m.deviceId === saved)) el.device.value = saved;
  return el.device.value;
}

function startMeter() {
  audioCtx = audioCtx || new AudioContext();
  const src = audioCtx.createMediaStreamSource(stream);
  analyser = audioCtx.createAnalyser();
  analyser.fftSize = 1024;
  src.connect(analyser);
  const buf = new Float32Array(analyser.fftSize);
  const tick = () => {
    analyser.getFloatTimeDomainData(buf);
    let sum = 0;
    for (const v of buf) sum += v * v;
    const rms = Math.sqrt(sum / buf.length);
    const db = 20 * Math.log10(rms || 1e-7);
    // -50 dB (near silence) to 0 dB (clipping) across the meter.
    const pct = Math.max(0, Math.min(100, ((db + 50) / 50) * 100));
    el.meter.style.width = pct + "%";
    el.meter.classList.toggle("hot", db > -6);
    meterRaf = requestAnimationFrame(tick);
  };
  tick();
}

function stopMeter() {
  if (meterRaf) cancelAnimationFrame(meterRaf);
  meterRaf = null;
  el.meter.style.width = "0%";
}

// --- the clip ---------------------------------------------------------------

function playClip(beat, onEnd) {
  if (!beat.video || beat.clipStart == null) {
    if (onEnd) onEnd();
    return;
  }
  stopClip();
  el.clip.currentTime = beat.clipStart;
  const watch = () => {
    if (el.clip.currentTime >= beat.clipEnd - 0.02) {
      stopClip();
      if (onEnd) onEnd();
    }
  };
  el.clip.addEventListener("timeupdate", watch);
  clipStopper = () => el.clip.removeEventListener("timeupdate", watch);
  el.clip.play().catch(() => {});
}

function stopClip() {
  el.clip.pause();
  if (clipStopper) clipStopper();
  clipStopper = null;
}

// --- recording --------------------------------------------------------------

async function startRecording() {
  if (!current || busy) return;
  busy = true;
  try {
    await openMic(el.device.value);
    await listDevices(el.device.value);     // labels appear after permission
  } catch (err) {
    busy = false;
    setStatus("no microphone: " + err.message, "err");
    return;
  }

  discardTake();
  el.record.textContent = "…";
  for (let n = COUNT_FROM; n > 0; n--) {
    el.countdown.hidden = false;
    el.countdown.textContent = n;
    await sleep(700);
  }
  el.countdown.hidden = true;

  chunks = [];
  const mime = pickMime();
  recorder = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
  recorder.ondataavailable = (e) => { if (e.data.size) chunks.push(e.data); };
  recorder.onstop = finishRecording;
  recorder.start();
  takeStart = performance.now();
  busy = false;

  el.recdot.hidden = false;
  el.record.textContent = "Stop";
  el.record.classList.add("recording");
  setStatus("recording — read the line, then stop");

  playClip(current);
  const tick = () => {
    const elapsed = (performance.now() - takeStart) / 1000;
    drawBand(current, elapsed);
    const { low, high } = band(current);
    el.note.innerHTML = `<b>${elapsed.toFixed(1)}s</b> · aim for ` +
      `<span class="good">${low.toFixed(1)}\u2013${high.toFixed(1)}s</span>`;
    bandRaf = requestAnimationFrame(tick);
  };
  tick();
}

function stopRecording() {
  if (recorder && recorder.state === "recording") recorder.stop();
}

function finishRecording() {
  if (bandRaf) cancelAnimationFrame(bandRaf);
  bandRaf = null;
  stopClip();
  el.recdot.hidden = true;
  el.record.textContent = "Record";
  el.record.classList.remove("recording");
  el.record.append(kbd("space"));

  takeBlob = new Blob(chunks, { type: recorder.mimeType || "audio/webm" });
  if (takeUrl) URL.revokeObjectURL(takeUrl);
  takeUrl = URL.createObjectURL(takeBlob);

  const elapsed = (performance.now() - takeStart) / 1000;
  drawBand(current, elapsed);
  describeBand(current, elapsed);
  el.keep.disabled = false;
  el.redo.disabled = false;
  el.hear.disabled = false;
  setStatus("listen back, then keep it or go again", "ok");
}

function pickMime() {
  const wanted = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg"];
  return wanted.find((m) => MediaRecorder.isTypeSupported(m)) || "";
}

function discardTake() {
  if (takeUrl) URL.revokeObjectURL(takeUrl);
  takeUrl = null;
  takeBlob = null;
  el.keep.disabled = true;
  el.redo.disabled = true;
}

// --- hearing it back --------------------------------------------------------

/* A take that has been kept is an mp3 on disk and an <audio> element plays it
   without complaint. A take still in hand is whatever MediaRecorder produced —
   webm/opus in Chrome, a fragmented mp4 in Safari — and a media element will
   refuse some of those outright ("no supported source was found") even though
   the recording is perfectly good. Decoding it ourselves sidesteps the
   element's source handling, so the same bytes play in either browser. */

async function playBuffer(blob) {
  audioCtx = audioCtx || new AudioContext();
  if (audioCtx.state === "suspended") await audioCtx.resume();
  const buffer = await audioCtx.decodeAudioData(await blob.arrayBuffer());
  const source = audioCtx.createBufferSource();
  source.buffer = buffer;
  source.connect(audioCtx.destination);
  source.onended = () => { stopClip(); reviewSource = null; };
  source.start();
  reviewSource = source;
}

function playElement(src) {
  return new Promise((resolve, reject) => {
    review = new Audio(src);
    review.onended = () => { stopClip(); resolve(); };
    review.onerror = () => reject(new Error("the browser would not load it"));
    review.play().then(resolve, reject);
  });
}

async function hear() {
  if (!current) return;
  stopReview();

  // Play it against the picture: the question is never whether the audio is
  // good on its own, but whether the read fits what is on screen.
  if (takeBlob) {
    if (takeBlob.size < 512) {
      setStatus("that take came back empty — check the microphone and the "
                + "input level, then record again", "err");
      return;
    }
    playClip(current);
    try {
      await playBuffer(takeBlob);
      setStatus("playing the take you just recorded", "ok");
      return;
    } catch (err) {
      try {
        await playElement(takeUrl);
        setStatus("playing the take you just recorded", "ok");
        return;
      } catch (second) {
        stopClip();
        setStatus(`could not play that take back (${err.message}). It is not `
                  + "lost — keep it and it will be converted to mp3.", "err");
        return;
      }
    }
  }

  if (current.status === "missing") {
    setStatus("nothing recorded for this line yet");
    return;
  }
  playClip(current);
  const kind = current.status === "scratch" ? "scratch" : "recorded";
  try {
    setStatus(`playing the ${kind} take against the animation`);
    await playElement(
      `/api/audio/${el.project.value}/${current.stem}?t=${Date.now()}`);
  } catch (err) {
    stopClip();
    setStatus("could not play: " + err.message, "err");
  }
}

function stopReview() {
  if (review) { review.pause(); review = null; }
  if (reviewSource) {
    reviewSource.onended = null;
    try { reviewSource.stop(); } catch (err) { /* already finished */ }
    reviewSource = null;
  }
  stopClip();
}

// --- keeping ----------------------------------------------------------------

async function keep() {
  if (!takeBlob || !current || busy) return;
  busy = true;
  const stem = current.stem;
  setStatus("saving…");
  try {
    const res = await fetch(`/api/take/${el.project.value}/${stem}`, {
      method: "POST",
      headers: {
        "Content-Type": takeBlob.type || "audio/webm",
        "X-Input-Device": deviceLabel(),
      },
      body: takeBlob,
    });
    const body = await res.json();
    if (!res.ok) throw new Error(body.error || res.status);
    discardTake();
    await load(stem);
    setStatus(`saved ${stem}.mp3 — ${body.speech.toFixed(2)}s of speech`, "ok");
    describeBand(beats.find((b) => b.stem === stem), body.speech);
    busy = false;
    nextToDo();
  } catch (err) {
    busy = false;
    setStatus("could not save: " + err.message, "err");
  }
}

async function undo() {
  if (!current || busy) return;
  busy = true;
  const stem = current.stem;
  try {
    const res = await fetch(`/api/take/${el.project.value}/${stem}`,
                            { method: "DELETE" });
    const body = await res.json();
    if (!res.ok) throw new Error(body.error || res.status);
    await load(stem);
    setStatus(`went back to the take from ${body.restored}`, "ok");
  } catch (err) {
    setStatus(err.message, "err");
  }
  busy = false;
}

function nextToDo() {
  const i = beats.findIndex((b) => b.stem === current.stem);
  const after = beats.slice(i + 1).find((b) => b.status !== "recorded");
  if (after) select(after.stem);
}

function deviceLabel() {
  const opt = el.device.selectedOptions[0];
  return opt ? opt.textContent : "";
}

// --- odds and ends ----------------------------------------------------------

function stopEverything() {
  stopRecording();
  stopReview();
  stopClip();
  if (bandRaf) cancelAnimationFrame(bandRaf);
  bandRaf = null;
}

function setStatus(text, kind) {
  el.status.textContent = text;
  el.status.className = "status" + (kind ? " " + kind : "");
}

function kbd(key) {
  const k = document.createElement("kbd");
  k.textContent = key;
  return k;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// --- wiring -----------------------------------------------------------------

el.record.onclick = () =>
  (recorder && recorder.state === "recording") ? stopRecording() : startRecording();
el.playclip.onclick = () => { stopReview(); playClip(current); };
el.hear.onclick = hear;
el.keep.onclick = keep;
el.redo.onclick = () => { discardTake(); startRecording(); };
el.undo.onclick = undo;

el.project.onchange = () => switchProject(el.project.value);

el.device.onchange = async () => {
  localStorage.setItem("booth.device", el.device.value);
  try { await openMic(el.device.value); } catch (err) {
    setStatus("could not open that microphone: " + err.message, "err");
  }
};

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "SELECT" || e.metaKey || e.ctrlKey) return;
  if (!current) return;
  const recording = recorder && recorder.state === "recording";
  const keys = {
    " ": () => recording ? stopRecording() : startRecording(),
    "Enter": () => !el.keep.disabled && keep(),
    "r": () => { discardTake(); startRecording(); },
    "p": () => hear(),
    "w": () => { stopReview(); playClip(current); },
    "u": () => undo(),
    "ArrowDown": () => step(1),
    "ArrowUp": () => step(-1),
    "j": () => step(1),
    "k": () => step(-1),
  };
  const fn = keys[e.key];
  if (!fn) return;
  e.preventDefault();
  fn();
});

function step(delta) {
  if (!current) return;
  const i = beats.findIndex((b) => b.stem === current.stem);
  const next = beats[i + delta];
  if (next) select(next.stem);
}

window.addEventListener("beforeunload", (e) => {
  if (takeBlob) { e.preventDefault(); e.returnValue = ""; }
});

// Ask for the microphone up front: the device list has no usable labels until
// permission is granted, and picking the wrong input is the easiest way to
// record 46 silent files.
(async function start() {
  try {
    await loadProjects();
  } catch (err) {
    setStatus(err.message, "err");
    return;
  }
  await load();
  try {
    await openMic();
    await listDevices();
    await openMic(el.device.value);
  } catch (err) {
    setStatus("microphone not available yet — click Record to allow it", "err");
    await listDevices();
  }
})();
