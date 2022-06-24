/*
    Created on : 12 May 2022, 15:42
    Author     : xhico
*/

async function setStatus(status, id) {
    $.ajax({
        type: "POST", url: "/workflow/status", data: {
            "id": id, "status": status
        }, success: function (entry) {
            console.log(entry);
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("ERROR");
        }
    });
}

window.addEventListener('DOMContentLoaded', async function main() {
    console.log("Starting");
    console.log("Get Workflow Details - " + workflow_id);
});