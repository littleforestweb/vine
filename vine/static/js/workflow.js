/*
    Created on : 03 May 2022, 17:57
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
    console.log("Get Workflow");

    // Reset Table
    $('#table').DataTable().clear().draw();
    $('#table').DataTable().destroy();

    let json = await $.get("/api/get_workflows", function (result) {
        return result;
    });

    // Set dataset
    let dataset = [];
    json = json["workflows"];
    for (let i = 0; i < json.length; i++) {
        let entry = json[i];
        let id = entry["id"];
        let startUser = entry["startUser"];
        let assignEditor = entry["assignEditor"];
        let comments = entry["comments"];
        let submittedDate = entry["submittedDate"].replace("GMT", "").trim();
        let status = entry["status"];
        dataset.push([id, id, startUser, assignEditor, comments, submittedDate, status, [id, status]]);
    }

    // Setup - add a text input to each header cell
    $('#table thead tr').clone(true).addClass('filters').appendTo('#table thead');
    let searchColumns = [1, 2, 3, 4, 6];

    $('#table').DataTable({
        dom: 'Brtip', buttons: {
            buttons: [{text: 'Export', extend: 'csv', filename: 'Workflow Report', className: 'btn-export'}], dom: {
                button: {
                    className: 'btn'
                }
            }
        }, paginate: false, "language": {"emptyTable": "No data available in table"}, "order": [[1, "desc"]], data: dataset, "autoWidth": false, initComplete: function () {
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
            "width": "10%", orderable: false, className: "center", "targets": 0, "render": function (data, type, row) {
                return "<input class='dt-checkboxes' id='checkbox_" + data + "' type='checkbox'>";
            }
        }, {
            "width": "10%", "targets": 1, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 2, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 3, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "20%", "className": "truncate", "targets": 4, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "20%", "targets": 5, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 6, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 7, "render": function (data, type, row) {
                let elem = "<a class='green-link' href='workflow_details?id=" + data[0] + "'>View</a><br>";
                if (data[1] !== "Approved" && data[1] !== "Rejected") {
                    elem += "<a class='green-link' href='#' onclick='setStatus(\"Approved\", " + data[0] + ")'>Approve</a><br><a class='green-link' href='#' onclick='setStatus(\"Rejected\" ," + data[0] + ")'>Reject</a>";
                }

                return elem
            },
        }]
    });
    $("#table_wrapper > .dt-buttons").prependTo("div.header-btns");

});