/*
    Created on : 02 Mar 2022, 09:59:17
    Author     : xhico
*/

async function publishSite() {
    $('#publishModal').modal('show');

    // Get all rows that are selected
    let checkedRows = $('#table').DataTable().rows(function (idx, data, node) {
        return $(node).find('.dt-checkboxes:input[type="checkbox"]').prop('checked');
    }).data().toArray();

    // Add ids to textarea inside publishModal
    let selectedIdsText = document.getElementById("selectedIds");
    selectedIdsText.innerText = "";
    checkedRows.forEach(function (row) {
        let siteId = row[0];
        selectedIdsText.innerText += siteId + " ";
    });
}

async function addWorkflow() {
    let siteIds = document.getElementById("selectedIds").value;
    let comments = document.getElementById("publishComments").value

    $.ajax({
        type: "POST", url: "/workflow/add", data: {
            "startUser": "123", "assignEditor": "321", "siteIds": siteIds, "comments": comments
        }, success: function (entry) {
            console.log(entry);
            document.getElementById("viewWorkflow").href = "/workflow_details?id=" + entry["workflow_id"];
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("ERROR");
        }
    });

    await showPublishNotification();
}

async function selectUserReviewer(user) {
    if (user.style.backgroundColor === "rgb(222, 226, 230)") {
        user.classList.add("bg-transparent");
        user.style.backgroundColor = "";
        document.getElementById("selectedUsers").value = document.getElementById("selectedUsers").value.replace(user.innerText + " ", "");
    } else {
        document.getElementById("selectedUsers").value += user.innerText + " ";
        user.classList.remove("bg-transparent");
        user.style.backgroundColor = "rgb(222, 226, 230)";
    }
}

async function showPublishNotification() {
    $('#publishModal').modal('hide');
    $('#publishedNotification').toast('show');
}

window.addEventListener('DOMContentLoaded', async function main() {
    console.log("Starting");
    console.log("Get Site");

    // Reset Table
    $('#table').DataTable().clear().draw();
    $('#table').DataTable().destroy();

    // Get siteJSON
    let json = await $.get("/api/get_site?id=" + site_id, function (result) {
        return result;
    });

    // Get base_url
    let base_url = json["site"]["base_url"];
    let base_folder = json["site"]["base_folder"];
    let getUrlFolder = base_url.replace(base_url.split("/").pop(), "");

    // Set pagesFolderName
    document.getElementById("TableName").innerText = base_folder;

    // Set dataset
    let dataset = [];
    json = json["pages"];
    for (let i = 0; i < json.length; i++) {
        let entry = json[i];
        let id = entry["id"];
        let title = entry["title"];
        let url = entry["url"];
        let modified_date = entry["modified_date"];
        let add_by = entry["add_by"];
        dataset.push([id, id, title, [id, url], modified_date, add_by, id]);
    }

    // Setup - add a text input to each header cell
    $('#table thead tr').clone(true).addClass('filters').appendTo('#table thead');
    let searchColumns = [2, 3, 4, 5];

    $('#table').DataTable({
        dom: 'Brtip', buttons: {
            buttons: [{text: 'Export', extend: 'csv', filename: 'Site Report', className: 'btn-export'}], dom: {
                button: {
                    className: 'btn'
                }
            }
        }, paginate: false, "language": {"emptyTable": "No data available in table"}, "order": [[0, "asc"]], data: dataset, "autoWidth": false, initComplete: function () {
            // For each column
            var api = this.api();
            api.columns().eq(0).each(function (colIdx) {
                // Set the header cell to contain the input element
                var cell = $('.filters th').eq($(api.column(colIdx).header()).index());
                if (searchColumns.includes(colIdx)) {
                    $(cell).html('<input type="text" placeholder="Search" />');
                } else {
                    $(cell).html('<span></span>');
                }

                // On every keypress in this input
                $('input', $('.filters th').eq($(api.column(colIdx).header()).index())).off('keyup change').on('keyup change', function (e) {
                    e.stopPropagation();
                    // Get the search value
                    $(this).attr('title', $(this).val());
                    var regexr = '({search})';
                    var cursorPosition = this.selectionStart;

                    // Search the column for that value
                    api.column(colIdx).search(this.value != '' ? regexr.replace('{search}', '(((' + this.value + ')))') : '', this.value != '', this.value == '').draw();
                    $(this).focus()[0].setSelectionRange(cursorPosition, cursorPosition);
                });
            });
        }, "columnDefs": [{
            "width": "5%", orderable: false, className: "center", "targets": 0, "render": function (data, type, row) {
                return "<input class='dt-checkboxes' id='checkbox_" + data + "' type='checkbox'>";
            }
        }, {
            "width": "100px", "className": "truncate max100px", "targets": 1, "render": function (data, type, row) {
                data = "/get_screenshot?id=" + data;
                return "<img src='" + data + "' width='100%' height='auto' alt='Page Screenshot Image'>"
            },
        }, {
            "width": "30%", "className": "truncate", "targets": 2, "render": function (data, type, row) {
                data = unescape(data);
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "30%", "className": "truncate", "targets": 3, "render": function (data, type, row) {
                let pathName = data[1].replace(getUrlFolder, "");
                return "<a class='green-link' target='_blank' href='/get_page?id=" + data[0] + "'>" + "/" + pathName + "</a>";
            },
        }, {
            "width": "10%", "targets": 4, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 5, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 6, "render": function (data, type, row) {
                data = "https://inspector.littleforest.co.uk:7777/get_page?id=" + data;
                return "<a class='green-link' target='_blank' href='https://inspector.littleforest.co.uk/DevWS/Inspector?url=" + data + "'>Inspect</a>" + " | " + "<a class='green-link' target='_blank' href='https://inspector.littleforest.co.uk/DevWS/Inspector?url=" + data + "&edit=true'>Edit</a>";
            },
        }]
    });
    $("#table_wrapper > .dt-buttons").prependTo("div.header-btns");
});