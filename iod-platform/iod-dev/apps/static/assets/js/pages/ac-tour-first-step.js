// main.js
import { checkAndUpdateLocalStorage,checkPreviousStepsCompleted,updateStepStatus } from './tour.js';

document.addEventListener("DOMContentLoaded", () => {
    
    const tourStatus = user_tour_status.toString();
    checkAndUpdateLocalStorage(tourStatus);
    //console.log("user requires tour : " + user_tour_status);
    if(user_tour_status.toString() === "Not-Started" || user_tour_status.toString() === "In-Progress") {
        if (localStorage.getItem('tour_step1_completed') !== 'yes') {
            startTour(1);
        }
        else if(checkPreviousStepsCompleted(3) == true &&  localStorage.getItem('tour_step3_completed') !== 'yes') {
            startTour(3);
        };
    }

    function startTour(stepNumber) {
        const intro = introJs();
        const steps = getSteps(stepNumber);
        intro.setOptions({ steps })
            .onexit(updateStepStatus.bind(null, stepNumber, 'Exited'))
            .oncomplete(updateStepStatus.bind(null, stepNumber, 'Completed'))
            .start();
    }

    function getSteps(stepNumber) {
        if (stepNumber === 1) {
            return [{
                element: document.querySelector('.sidebar-settings-step1'),
                intro: "Welcome to InvestODiary.com. I will help you get started. Please click on Settings - option on the sidebar ",
            }];
        } else if (stepNumber === 3) {
            return [{
                element: document.querySelector('.networth-summary-step1'),
                intro: "Great, Now you can plan and track your investments",
            }, {
                element: document.querySelector('.networth-summary-step2'),
                intro: "Right now you do not have any categories set up, lets fix that ",
            }, {
                element: document.querySelector('.edit-networth-step3'),
                intro: "Click on Edit Networth ",
            }];
        }
    }
});

