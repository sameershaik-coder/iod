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
    //RUN THE TOUR
    if (localStorage.getItem('tour_step4_completed') !== 'yes') {
        var intro = introJs();
        intro.setOptions({
            steps: [{
                intro: "This is your Networth configuration page. You can add,edit or delete a category here",
            }, 
            {
                element: document.querySelector('.add-button-step1'),
                intro: "Click on Add button and add a category for your funds - for example : Mutual Funds"
            }
        ]
        })
        .onexit(function() {
            // Code to disable the tour when it's exited
            //localStorage.setItem('tour_step4_completed_skip', 'no');
            // localStorage.setItem('tour_step5_completed', 'no');
            
        })
        .oncomplete(function() {
            // Code to disable the tour when it's completed
            let status = 'completed';  // The new step status
            fetch('/update_step_status/', {
                method: 'POST',
                body: JSON.stringify({
                    'name' : '4',
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
                    localStorage.setItem('tour_step4_completed', 'yes');
                }
                //console.log(data.status);
            });
            
        })
        .start();
    }
    window.onload = function() {
        var table = document.getElementById("tbl_categories"); // replace with your table id
        if(table!=null){
            var rowCount = table.rows.length;
            //console.log("Number of rows in the table: " + rowCount);
            if (localStorage.getItem('tour_step5_completed') !== 'yes') {
                var intro = introJs();
                intro.setOptions({
                    steps: [
                        {
                        intro: "Congrats you have added a new Category",
                    }, 
                    {
                        element: document.querySelector('.view-button-step2'),
                        intro: "Click on View"
                    }
                ]
                })
                .onexit(function() {
                    // Code to disable the tour when it's exited
                    //localStorage.setItem('tour_step5_completed', 'yes');
                    
                })
                .oncomplete(function() {
                    // Code to disable the tour when it's completed
                    let status = 'completed';  // The new step status
                    fetch('/update_step_status/', {
                        method: 'POST',
                        body: JSON.stringify({
                            'name' : '5',
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
                            localStorage.setItem('tour_step5_completed', 'yes');
                        }
                        //console.log(data.status);
                    });
                    
                })
                .start();
            }
        }
    };

    
});