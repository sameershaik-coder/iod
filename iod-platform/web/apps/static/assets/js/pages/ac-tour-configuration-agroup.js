// main.js
import { checkAndUpdateLocalStorage,checkPreviousStepsCompleted,updateStepStatus } from './tour.js';

document.addEventListener("DOMContentLoaded", () => {
    
    const tourStatus = user_tour_status.toString();
    checkAndUpdateLocalStorage(tourStatus);
    //console.log("user requires tour : " + user_tour_status);
    if(user_tour_status.toString() === "Not-Started" || user_tour_status.toString() === "In-Progress") {
        if (checkPreviousStepsCompleted(8) == true && localStorage.getItem('tour_step8_completed') !== 'yes') {
            startTour(8);
        }
        else if(checkPreviousStepsCompleted(9) == true &&  localStorage.getItem('tour_step9_completed') !== 'yes') {
            startTour(9);
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
        if (stepNumber === 8) {
            return [
                {
                    intro: "You can add, edit or delete an instrument here",
                }, 
                {
                    element: document.querySelector('.add-button-step1'),
                    intro: "Click on Add button and add an instrument from your funds - for example : PPFAS Tax Saver, HDFC Bank or Gold ETF "
                }
        ];
        } else if (stepNumber === 9) {

            var table = document.getElementById("tbl_instruments"); // replace with your table id
            if(table!=null){
                // var rowCount = table.rows.length;
                // console.log(rowCount);
                return [
                    {
                        intro: "Congrats you have added a new Instrument",
                    }, 
                    {
                        intro: "Yay! We have come to the end of the tour. Happy Investing :)",
                    }, 
                    {
                        element: document.querySelector('.nav-networth-summary-step2'),
                        intro: "Click on Networth Summary and review your investments"
                    }
            ];
            }
        }
    }
});

