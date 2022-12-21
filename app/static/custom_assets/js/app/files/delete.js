"use strict";
let delete_link = document.querySelectorAll('[data-kt-filemanager-table-filter="delete_row"]');
let table = $("#kt_file_manager_list").DataTable();
function popupFileDelete(message, type){
    return Swal.fire({
        text: message,
        icon: type,
        buttonsStyling: false,
        confirmButtonText: "Ok, got it!",
        customClass: {
            confirmButton: "btn fw-bold btn-primary"
        }
    })
}
async function deleteFile(url, n, o){
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append("delete_files", [o.querySelectorAll(".sorting_1>div>input")[0].value]);
    const response = await fetch(url, {
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
    });
    if(response.status === 200){
        popupFileDelete("You have deleted "+n+"!.","success").then((function(){
            table.row($(o)).remove().draw();
            location.reload();
        }));
    }
    else{
        popupFileDelete("Something wrong! Please perform again!","error").then(()=>{
            location.reload();
        });
    }
}
delete_link.forEach(t=>{
    t.addEventListener("click", (e) => {
        e.preventDefault();
        const o=t.closest("tr");
        const n=o.querySelectorAll("td")[1].innerText;
        Swal.fire({
            text:"Are you sure you want to delete "+n+"?",
            icon:"warning",
            showCancelButton:!0,
            buttonsStyling:!1,
            confirmButtonText:"Yes, delete!",
            cancelButtonText:"No, cancel",
            customClass:{
                confirmButton:"btn fw-bold btn-danger",
                cancelButton:"btn fw-bold btn-active-light-primary"
            }
        }).then((result)=>{
            if(result.isConfirmed) {
                deleteFile('/project/deletefile/', n,o).then(r => {console.log(r)});
            } else {
                popupFileDelete(n+" was not deleted.","error");
            }
        });
    })
});