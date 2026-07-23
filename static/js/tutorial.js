// static/js/tutorial.js — AI Guide onboarding tutorial
// Highlights dashboard elements one-by-one with an explanation tooltip.
// Steps are read from data-tutorial="stepKey" attributes on elements in dashboard.html.

const TUTORIAL_STEPS = [
  { key: "submit-idea", text: "Click here to submit your project idea. Just describe what you want to build, in plain English." },
  { key: "my-projects", text: "All the projects you've generated live here — pick up where you left off anytime." },
  { key: "ai-assistant", text: "This is me! Come back here anytime you're stuck or have a question." },
  { key: "mentor", text: "Click here to find a mentor who can guide you through your project." },
  { key: "similar-projects", text: "See similar existing projects here, so you can learn from what's already out there." },
  { key: "documentation", text: "Click here to generate full documentation for your project automatically." },
  { key: "ppt-generator", text: "Need a presentation? This generates a ready-to-use PPT outline for your project." },
  { key: "profile", text: "Your profile tracks your submitted projects, saved projects, and overall progress." },
];

let currentStep = 0;

function startTutorial() {
  currentStep = 0;
  document.getElementById("tutorialOverlay").classList.add("active");
  showStep(currentStep);
}

function showStep(index) {
  if (index >= TUTORIAL_STEPS.length) {
    endTutorial(true);
    return;
  }
  const step = TUTORIAL_STEPS[index];
  const target = document.querySelector(`[data-tutorial="${step.key}"]`);
  const spotlight = document.getElementById("tutorialSpotlight");
  const tooltip = document.getElementById("tutorialTooltip");

  if (!target) {
    // Skip missing targets gracefully
    currentStep++;
    showStep(currentStep);
    return;
  }

  target.scrollIntoView({ behavior: "smooth", block: "center" });

  // Give scroll a moment to settle before measuring position
  setTimeout(() => {
    const rect = target.getBoundingClientRect();
    const pad = 8;

    spotlight.style.top = `${rect.top - pad}px`;
    spotlight.style.left = `${rect.left - pad}px`;
    spotlight.style.width = `${rect.width + pad * 2}px`;
    spotlight.style.height = `${rect.height + pad * 2}px`;

    let tooltipTop = rect.bottom + 16;
    let tooltipLeft = rect.left;
    if (tooltipLeft + 300 > window.innerWidth) tooltipLeft = window.innerWidth - 320;
    if (tooltipTop + 200 > window.innerHeight) tooltipTop = rect.top - 200;

    tooltip.style.top = `${tooltipTop}px`;
    tooltip.style.left = `${Math.max(16, tooltipLeft)}px`;

    document.getElementById("tutorialText").textContent = step.text;
    document.getElementById("tutorialProgress").textContent = `${index + 1} of ${TUTORIAL_STEPS.length}`;
    document.getElementById("tutorialBackBtn").style.visibility = index === 0 ? "hidden" : "visible";
    document.getElementById("tutorialNextBtn").textContent = index === TUTORIAL_STEPS.length - 1 ? "Finish" : "Next";
  }, 250);
}

function nextStep() {
  currentStep++;
  showStep(currentStep);
}

function prevStep() {
  if (currentStep > 0) {
    currentStep--;
    showStep(currentStep);
  }
}

function endTutorial(completed) {
  document.getElementById("tutorialOverlay").classList.remove("active");
  if (completed) {
    fetch("/tutorial/complete", { method: "POST" }).catch(() => {});
  }
}

function closeAiWelcome(startNow) {
  document.getElementById("aiWelcomeModal").classList.remove("active");
  if (startNow) {
    startTutorial();
  } else {
    fetch("/tutorial/complete", { method: "POST" }).catch(() => {});
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("aiWelcomeModal");
  if (modal && modal.dataset.show === "true") {
    modal.classList.add("active");
  }
});
