// static/js/chat.js

const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const stopMicBtn = document.getElementById("stopMicBtn");
const eligibilityForm = document.getElementById("eligibilityForm");
const efSubjects = document.getElementById("ef-subjects");
const efPercentage = document.getElementById("ef-percentage");
const efYears = document.getElementById("ef-years");
const efCategory = document.getElementById("ef-category");
const efSubmit = document.getElementById("ef-submit");
const efCancel = document.getElementById("ef-cancel");

let recognition = null;
let isRecognizing = false;

// Initialize Web Speech API (SpeechRecognition) if available
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    isRecognizing = true;
    micBtn.style.display = "none";
    stopMicBtn.style.display = "inline-block";
    addSystemMessage("Listening... Speak now.");
  };

  recognition.onend = () => {
    isRecognizing = false;
    micBtn.style.display = "inline-block";
    stopMicBtn.style.display = "none";
  };

  recognition.onerror = (e) => {
    isRecognizing = false;
    micBtn.style.display = "inline-block";
    stopMicBtn.style.display = "none";
    addSystemMessage("Speech recognition error: " + e.error);
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    sendText(transcript);
  };
} else {
  micBtn.disabled = true;
  addSystemMessage("Voice input not supported in this browser. Use Chrome or Edge for speech features.");
}

function addMessage(text, who="bot"){
  const d = document.createElement("div");
  d.className = `message ${who==='bot'?'bot':'user'}`;
  d.innerHTML = `<div>${escapeHtml(text).replace(/\n/g,'<br>')}</div>`;
  chatbox.appendChild(d);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function addSystemMessage(text){
  const d = document.createElement("div");
  d.className = `message bot`;
  d.style.opacity = "0.7";
  d.innerHTML = `<div><em>${escapeHtml(text)}</em></div>`;
  chatbox.appendChild(d);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function escapeHtml(unsafe) {
  return String(unsafe)
       .replaceAll("&", "&amp;")
       .replaceAll("<", "&lt;")
       .replaceAll(">", "&gt;")
       .replaceAll('"', "&quot;")
       .replaceAll("'", "&#039;");
}

async function sendText(msg){
  addMessage(msg, "user");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    const reply = data.reply || "No reply.";
    addMessage(reply, "bot");

    // Speak the reply using SpeechSynthesis
    speakText(reply);

    if (data.meta && data.meta.show_form){
      eligibilityForm.classList.remove("hidden");
      if (data.meta.show_form === "comedk"){
        efYears.parentElement.style.display = "none";
      } else {
        efYears.parentElement.style.display = "block";
      }
    } else {
      eligibilityForm.classList.add("hidden");
    }
  } catch (err) {
    addSystemMessage("Network or server error: " + err.message);
  }
}

sendBtn.onclick = () => {
  const text = userInput.value.trim();
  if (!text) return;
  userInput.value = "";
  sendText(text);
};

userInput.addEventListener("keydown", (e)=>{
  if (e.key === "Enter") { sendBtn.click(); }
});

document.querySelectorAll(".quick").forEach(btn=>{
  btn.addEventListener("click", ()=> sendText(btn.getAttribute("data-msg")));
});

document.getElementById("kcetBtn").onclick = ()=> sendText("I want to check KCET eligibility.");
document.getElementById("comedkBtn").onclick = ()=> sendText("I want to check COMED-K eligibility.");

efCancel.onclick = ()=>{ eligibilityForm.classList.add("hidden"); };

efSubmit.onclick = ()=>{
  const subj = efSubjects.value.trim();
  const pct = efPercentage.value.trim();
  const yrs = efYears.value.trim() || "0";
  const cat = efCategory.value.trim() || "general";
  if (!subj || !pct) { alert("Please fill subjects and percentage."); return; }
  const structured = `subjects: ${subj}; percentage: ${pct}; years: ${yrs}; category: ${cat}`;
  eligibilityForm.classList.add("hidden");
  sendText(structured);
};

// Speech controls
micBtn.onclick = () => {
  if (!recognition) { addSystemMessage("SpeechRecognition not supported."); return; }
  try {
    recognition.start();
  } catch(e) {
    addSystemMessage("Could not start recognition: " + e.message);
  }
};

stopMicBtn.onclick = () => {
  if (recognition && isRecognizing) recognition.stop();
};

// TTS: use SpeechSynthesis
function speakText(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel(); // stop previous
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = "en-IN";
  // optional voice selection:
  // const voices = window.speechSynthesis.getVoices();
  // utter.voice = voices.find(v => v.lang === 'en-IN') || voices[0];
  window.speechSynthesis.speak(utter);
}
