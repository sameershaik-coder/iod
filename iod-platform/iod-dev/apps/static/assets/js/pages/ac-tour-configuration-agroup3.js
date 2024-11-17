'use strict';
document.addEventListener("DOMContentLoaded", function () {
    // Check if the tour has been completed
    if(user_tour_status.toString() == "Not-Started") {
        for (let i = 1; i < 10; i++) {
            let step_name = "tour_step" + i.toString() + "_completed";
            localStorage.setItem(step_name, 'no');
        }
    };
    if(user_tour_status.toString() == "In-Progress") {

        let jsonArrayString = '[{"name": "step1", "status": "completed"}, {"name": "step2", "status": "not started"}]';
        let jsonArray = JSON.parse(jsonArrayString);
        let user_tour_steps_list = JSON.parse(user_tour_steps_json);
        for(let i = 0; i < user_tour_steps_list.length; i++) {
            
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

    // RUN THE TOUR
    if (localStorage.getItem('tour_step8_completed') !== 'yes') {
        var intro = introJs();
        intro.setOptions({
            steps: [{
                intro: "You can add, edit or delete an instrument here",
            }, 
            {
                element: document.querySelector('.add-button-step1'),
                intro: "Click on Add button and add an instrument from your funds - for example : PPFAS Tax Saver, HDFC Bank or Gold ETF "
            }
        ]
        })
        .onexit(function() {
            // Code to disable the tour when it's exited
            
            
        })
        .oncomplete(function() {
            // Code to disable the tour when it's completed
            
            let status = 'completed';  // The new step status
            fetch('/update_step_status/', {
                method: 'POST',
                body: JSON.stringify({
                    'name' : '8',
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
                    localStorage.setItem('tour_step8_completed', 'yes');
                }
                //console.log(data.status);
            });
            
        })
        .start();
    }
    window.onload = function() {
        var table = document.getElementById("tbl_instruments"); // replace with your table id
        if(table!=null){
            var rowCount = table.rows.length;
            //console.log("Number of rows in the table: " + rowCount);
            if (localStorage.getItem('tour_step9_completed') !== 'yes') {
                var intro = introJs();
                intro.setOptions({
                    steps: [
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
                ]
                })
                .onexit(function() {
                    // Code to disable the tour when it's exited
                    
                    
                })
                .oncomplete(function() {
                    // Code to disable the tour when it's completed
                    //localStorage.setItem('tour_step9_completed', 'yes');

                    let status = 'completed';  // The new step status
                    fetch('/update_step_status/', {
                        method: 'POST',
                        body: JSON.stringify({
                            'name' : '9',
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
                            localStorage.setItem('tour_step9_completed', 'yes');
                        }
                        //console.log(data.status);
                    });
                    
                })
                .start();
            }
        }
    };

    
});