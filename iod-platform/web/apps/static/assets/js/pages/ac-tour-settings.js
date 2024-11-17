// main.js
import { checkAndUpdateLocalStorage,checkPreviousStepsCompleted,updateStepStatus } from './tour.js';

document.addEventListener("DOMContentLoaded", () => {
    
    const tourStatus = user_tour_status.toString();
    checkAndUpdateLocalStorage(tourStatus);
    //console.log("user requires tour : " + user_tour_status);
    if(user_tour_status.toString() === "Not-Started" || user_tour_status.toString() === "In-Progress") {
        if(checkPreviousStepsCompleted(2) == true &&  localStorage.getItem('tour_step2_completed') !== 'yes') {
            startTour(2);
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
        if (stepNumber === 2) {
            return [
                {
                    intro: "This is your networth settings. Here you can set up amount of your total networth. Currently it is set to 1 ",
                }, 
                {
                    element: document.querySelector('.edit-button-step1'),
                    intro: "You can update your networth anytime using Edit"
                }, 
                {
                    element: document.querySelector('.networth-amount-step2'),
                    intro: "If you do not have exact number, you can just give an approximate number"
                },
                {
                    element: document.querySelector('.networth-base-unit-step3'),
                    intro: "Also notice that currently unit is set to default unit based on your country, you can edit this as well"
                },
                {
                    element: document.querySelector('.networth-table-step2'),
                    intro: "After you complete this settings, click on Networth Summary on the sidebar"
                }
            ];
        }
    }
});

