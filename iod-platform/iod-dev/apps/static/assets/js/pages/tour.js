// tour.js
'use strict';

export function initializeTourSteps() {
    for (let i = 1; i <= 9; i++) {
        localStorage.setItem(`tour_step${i}_completed`, 'no');
    }
}

export function updateTourSteps(user_tour_steps_json) {
    const userTourSteps = JSON.parse(user_tour_steps_json);

    userTourSteps.forEach(step => {
        const stepDesc = `tour_step${step.fields.step_name}_completed`;
        const stepStatus = step.fields.status === "Completed" ? 'yes' : 'no';
        localStorage.setItem(stepDesc, stepStatus);
    });
}

export function checkAndUpdateLocalStorage(tourStatus){
    //console.log(`User requires tour: ${tourStatus}`);

    if (tourStatus === "Not-Started") {
        initializeTourSteps();
    } else if (tourStatus === "Completed") {
        localStorage.clear();
    } else if (tourStatus === "In-Progress") {
        updateTourSteps(user_tour_steps_json);
    }
}

export function checkPreviousStepsCompleted(stepNumber){
    for(let i = 1; i < stepNumber; i++) {
        let stepname = 'tour_step'+i.toString()+'_completed';
        //console.log(stepname);
        let stepStatus = localStorage.getItem(stepname);
        //console.log(stepStatus);
        if(stepStatus !== 'yes') {
            return false;
        }
    }
    return true;
}

export function updateStepStatus(stepNumber, statusType) {
    let status = statusType === 'Completed' ? 'completed' : 'exited';  // The new step status
    fetch('/app/update_step_status/', {
        method: 'POST',
        body: JSON.stringify({
            'name' : stepNumber.toString(),
            'status': status.charAt(0).toUpperCase() + status.slice(1)
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // You need to include CSRF token in your requests
        }
    })
    .then(response => response.json())    
    .then(data => {
        if(data.status.toString() === "success") {
            localStorage.setItem(`tour_step${stepNumber}_completed`, 'yes');
        }
    });
}