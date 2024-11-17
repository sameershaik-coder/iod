'use strict';
document.addEventListener("DOMContentLoaded", function () {
    // Check if the tour has been completed
    console.log("user requires tour : " + user_tour_status);
    if(user_tour_status.toString() == "Not-Started") {
        for (let i = 1; i < 10; i++) {
            let step_name = "tour_step" + i.toString() + "_completed";
            console.log(step_name);
            localStorage.setItem(step_name, 'no');
        }
    };
    if(user_tour_status.toString() == "In-Progress") {

        let jsonArrayString = '[{"name": "step1", "status": "completed"}, {"name": "step2", "status": "not started"}]';
        console.log(jsonArrayString);
        console.log(user_tour_steps_json);
        let jsonArray = JSON.parse(jsonArrayString);
        let user_tour_steps_list = JSON.parse(user_tour_steps_json);
        
        console.log(user_tour_steps_list);

        console.log("inside set up of : " + user_tour_status);
        //console.log(userTourSteps);
        for(let i = 0; i < user_tour_steps_list.length; i++) {
            console.log(user_tour_steps_list[i].fields.status); 
            let step_status = user_tour_steps_list[i].fields.status;
            let step_name = user_tour_steps_list[i].fields.step_name;
            let step_desc = 'tour_step'+step_name+'_completed';
            if(step_status == "Completed")
            {
                localStorage.setItem(step_desc, 'yes');
            }
            else
            {
                localStorage.setItem(step_desc, 'no');
            }  
        };
        
    };

    // Run the tour
    if (localStorage.getItem('tour_step2_completed') !== 'yes') {
        var intro = introJs();
        intro.setOptions({
            steps: [{
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
        ]
        })
        .onexit(function() {
            // Code to disable the tour when it's exited
            localStorage.setItem('tour_step2_completed', 'yes');
            //localStorage.setItem('tour_step3_completed', 'no');
        })
        .oncomplete(function() {
            // Code to disable the tour when it's completed
            localStorage.setItem('tour_step2_completed', 'yes');
            let status = 'completed';  // The new step status
            fetch('/update_step_status/', {
                method: 'POST',
                body: JSON.stringify({
                    'name' : '2',
                    'status': 'Completed'
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken  // You need to include CSRF token in your requests
                }
            })
            .then(response => response.json())    
            .then(data => {
                if(data.status.toString() === "success") {
                    localStorage.setItem('tour_step2_completed', 'yes');
                }
                console.log(data.status);
            });


        })
        .start();
    }
});