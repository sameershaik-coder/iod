// main.js
import { checkAndUpdateLocalStorage,checkPreviousStepsCompleted,updateStepStatus } from './tour.js';

document.addEventListener("DOMContentLoaded", () => {
    
    const tourStatus = user_tour_status.toString();
    checkAndUpdateLocalStorage(tourStatus);
    //console.log("user requires tour : " + user_tour_status);
    if(user_tour_status.toString() === "Not-Started" || user_tour_status.toString() === "In-Progress") {
        if (checkPreviousStepsCompleted(4) == true && localStorage.getItem('tour_step4_completed') !== 'yes') {
            startTour(4);
        }
        else if(checkPreviousStepsCompleted(5) == true &&  localStorage.getItem('tour_step5_completed') !== 'yes') {
            startTour(5);
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
        if (stepNumber === 4) {
            return [
                {
                    intro: "This is your Networth configuration page. You can add,edit or delete a category here",
                }, 
                {
                    element: document.querySelector('.add-button-step1'),
                    intro: "Click on Add button and add a category for your funds - for example : Mutual Funds"
                }
        ];
        } else if (stepNumber === 5) {

            var table = document.getElementById("tbl_categories"); // replace with your table id
            if(table!=null){
                // var rowCount = table.rows.length;
                // console.log(rowCount);
                return [
                    {
                        intro: "Congrats you have added a new Category",
                    }, 
                    {
                        element: document.querySelector('.view-button-step2'),
                        intro: "Click on View"
                    }
            ];
            }
        }
    }
});

