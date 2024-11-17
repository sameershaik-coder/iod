// main.js
import { checkAndUpdateLocalStorage,checkPreviousStepsCompleted,updateStepStatus } from './tour.js';

document.addEventListener("DOMContentLoaded", () => {
    
    const tourStatus = user_tour_status.toString();
    checkAndUpdateLocalStorage(tourStatus);
    //console.log("user requires tour : " + user_tour_status);
    if(user_tour_status.toString() === "Not-Started" || user_tour_status.toString() === "In-Progress") {
        if (checkPreviousStepsCompleted(6) == true && localStorage.getItem('tour_step6_completed') !== 'yes') {
            startTour(6);
        }
        else if(checkPreviousStepsCompleted(7) == true &&  localStorage.getItem('tour_step7_completed') !== 'yes') {
            startTour(7);
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
        if (stepNumber === 6) {
            return [
                {
                    intro: "You can add,edit or delete a sub-category also called Asset-Group here",
                }, 
                {
                    element: document.querySelector('.add-button-step1'),
                    intro: "Click on Add button and add a sub-category for your funds - for example : Large Cap MF, Momentum Stocks or Gold "
                }
        ];
        } else if (stepNumber === 7) {

            var table = document.getElementById("tbl_agroups"); // replace with your table id
            if(table!=null){
                // var rowCount = table.rows.length;
                // console.log(rowCount);
                return [
                    {
                        intro: "Congrats you have added a new Sub-Category",
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

