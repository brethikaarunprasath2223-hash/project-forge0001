// Project Forge main.js

document.addEventListener("DOMContentLoaded", function(){

    initThemeToggle();
    initMobileSidebar();
    initIdeaChips();

});


// ================= THEME TOGGLE =================

function initThemeToggle(){

    const body = document.body;
    const themeBtn = document.getElementById("themeToggle");

    if(!themeBtn) return;


    let savedTheme = localStorage.getItem("pf-theme");


    if(savedTheme === "dark"){
        body.classList.add("dark-mode");
        themeBtn.innerHTML = "☀️";
    }


    themeBtn.addEventListener("click", function(){

        body.classList.toggle("dark-mode");


        if(body.classList.contains("dark-mode")){

            localStorage.setItem("pf-theme","dark");
            themeBtn.innerHTML="☀️";

        }
        else{

            localStorage.setItem("pf-theme","light");
            themeBtn.innerHTML="🌙";

        }

    });

}



// ================= MOBILE SIDEBAR =================

function initMobileSidebar(){

    const btn=document.getElementById("mobileToggle");
    const sidebar=document.getElementById("sidebar");


    if(!btn || !sidebar) return;


    btn.onclick=function(){

        sidebar.classList.toggle("open");

    }

}



// ================= IDEA CHIPS =================

function initIdeaChips(){

    const chips=document.querySelectorAll(".idea-chip");
    const input=document.getElementById("ideaText");


    if(!input) return;


    chips.forEach(function(chip){

        chip.onclick=function(){

            input.value=chip.dataset.idea;
            input.focus();

        }

    });

}



// ================= HUMAN MENTOR =================


function openHumanMentor(){

    let box=document.getElementById("humanMentorChat");

    if(box){

        box.style.display="block";

    }

}



function closeHumanMentor(){

    let box=document.getElementById("humanMentorChat");

    if(box){

        box.style.display="none";

    }

}



function sendMentorQuestion(){

    let input=document.getElementById("mentorQuestion");
    let chat=document.getElementById("mentorMessages");


    if(!input || !chat) return;


    let msg=input.value.trim();


    if(msg==="") return;



    chat.innerHTML += `
    <p>
    🧑 You: ${msg}
    </p>
    `;


    chat.innerHTML += `
    <p>
    👨‍🏫 Mentor: I will guide you step by step for your project.
    </p>
    `;


    input.value="";


}



// ================= AI TOUR =================


let aiStep=0;


function nextAITour(){

    console.log("Next AI Tour");

}



function skipAITour(){

    let box=document.getElementById("aiTutorial");


    if(box){

        box.style.display="none";

    }

    localStorage.setItem("aiTourDone","yes");

}


console.log("MAIN JS LOADED");