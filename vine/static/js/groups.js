/*
    Created on : 21 Apr 2022, 09:25:00
    Author     : RJA
*/

async function clearAddGroupsDialog() {
    //console.log("clearAddGroupsDialog() START");

    //gns = $('#group-name');
    //gn = gns[0];
    //gnv = gn.value;
    //gnall = $('#group-name')[0].value;
    //console.log(gns);
    //console.log(gn);
    //console.log(gnv);
    //console.log(gnall);

    $('#group-name').val("");
    $('#group-display-name').val("");
    $('#group-description').val("");
    $('#group-id').val("");
    //console.log($('#group-display-name')[0].value);
    //console.log($('#group-description')[0].value);
    //console.log($('#group-id')[0].value);

    //console.log("clearAddGroupsDialog() END");
}

async function deleteGroups() {
    console.log("deleteGroups() : START");

    let checked_groups = [];
    let checked_groups_str = "";

    $.each($("input:checked"), function (K, V) {
        checked_groups.push(V.value);
        checked_groups_str += V.value + ",";
        console.log("deleteGroups() : END");
    });
    checked_groups_str = checked_groups_str.slice(0, -1);

    // Post
    $.ajax({
        type: "POST", url: "/delete/groups", data: {
            "groups_to_delete": checked_groups_str
        }, success: function (entry) {

            // Show success notification
            $('#deleteGroupSuccessNotification').toast('show');
            // Refresh page
            setTimeout(function () {
                location.reload(true);
            }, 2000);
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            // Hide Create Modal
            $('#addGroupModal').modal('hide');

            // Show Error Modal
            $('#errorModal').modal('show');

        }
    });

    console.log("deleteGroups() : END");
}

async function getSelectedGroupData() {
    console.log("getSelectedGroupData() START");
    console.log("getSelectedGroupData() END");
}

async function populateEditGroupModal() {
    console.log("populateEditGroupModal() START");

    let checked_items = $("input:checked");
    let n_checked_items = checked_items.length;
    let row = checked_items.parent().parent();
    console.log("n checked_items = " + checked_items.length);
    console.log("row html = " + row.html());
    console.log("row text = " + row.text());

    let spans = row.find("span");
    console.log("spans = " + spans.length);
    console.log(spans.text());

    let group_name = spans[0].textContent;
    let group_display_name = spans[1].textContent;
    let group_description = spans[2].textContent;
    let group_id = spans[3].textContent;
    console.log(group_name);
    console.log(group_display_name);
    console.log(group_description);
    console.log(group_id);

    // Populate edit fields
    $('#e-group-name').val(group_name);
    $('#e-group-display-name').val(group_display_name);
    $('#e-group-description').val(group_description);
    $('#e-group-id').val(group_id);

    // Populate hidden fields (for reference)
    $('#h-e-group-name').val(group_name);
    $('#h-e-group-display-name').val(group_display_name);
    $('#h-e-group-description').val(group_description);
    $('#h-e-group-id').val(group_id);

    console.log("populateEditGroupModal() END");
}

async function updateGroup() {
    let e_group_name = document.getElementById("e-group-name").value;
    let e_group_display_name = document.getElementById("e-group-display-name").value;
    let e_group_description = document.getElementById("e-group-description").value;
    let e_group_id = document.getElementById("e-group-id").value;

    let h_e_group_name = document.getElementById("h-e-group-name").value;
    let h_e_group_display_name = document.getElementById("h-e-group-display-name").value;
    let h_e_group_description = document.getElementById("h-e-group-description").value;
    let h_e_group_id = document.getElementById("h-e-group-id").value;

    console.log("Updating group from : " + h_e_group_name + " / " + h_e_group_display_name + " / " + h_e_group_description + " / " + h_e_group_id);
    console.log("Updating group with : " + e_group_name + " / " + e_group_display_name + " / " + e_group_description + " / " + e_group_id);

    // Post
    $.ajax({
        type: "POST", url: "/update/group", data: {
            "original_name": h_e_group_name, "original_description": h_e_group_description, "original_group_id": h_e_group_id, "original_group_display_name": h_e_group_display_name, "new_name": e_group_name, "new_description": e_group_description, "new_group_id": e_group_id, "new_group_display_name": e_group_display_name
        }, success: function (entry) {

            // Hide Create Modal
            $('#editGroupModal').modal('hide');

            // Show success notification
            $('#editGroupSuccessNotification').toast('show');

            // Refresh page
            setTimeout(function () {
                location.reload(true);
            }, 2000);
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            // Hide Create Modal
            $('#editGroupModal').modal('hide');

            // Show Error Modal
            $('#errorModal').modal('show');
        }
    });
}

async function addGroup() {
    let group_name = document.getElementById("group-name").value;
    let group_display_name = document.getElementById("group-display-name").value;
    let group_description = document.getElementById("group-description").value;
    let group_id = document.getElementById("group-id").value;

    // Post
    $.ajax({
        type: "POST", url: "/add/group", data: {
            "name": group_name, "description": group_description, "group_id": group_id, "group_display_name": group_display_name
        }, success: function (entry) {
            // Add row to Table
            let group_name = entry["name"];
            let group_display_name = entry["display_name"];
            let group_description = entry["description"];
            let group_id = entry["id"];
            $('#table').DataTable().row.add(["", group_name, group_display_name, group_description, group_id]).order([0, 'desc']).draw();

            // Hide Create Modal
            $('#addGroupModal').modal('hide');

            // Show success notification
            $('#addGroupSuccessNotification').toast('show');

            // Refresh page
            //setTimeout(function(){ location.reload(true); }, 2000);
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            // Hide Create Modal
            $('#addGroupModal').modal('hide');

            // Show Error Modal
            $('#errorModal').modal('show');
        }
    });
}

window.addEventListener('DOMContentLoaded', async function main() {
    console.log("Starting");
    console.log("Get Groups");

    // Reset pagesTable
    $('#table').DataTable().clear().draw();
    $('#table').DataTable().destroy();

    // Get pagesJSON
    let json = await $.get("/api/get_groups", function (result) {
        return result;
    });

    // Set dataset
    let dataset = [];
    json = json["groups"];
    for (let i = 0; i < json.length; i++) {
        let entry = json[i];
        let id = entry["id"];
        let group_name = entry["name"];
        let group_display_name = entry["display_name"];
        let group_description = entry["description"];
        dataset.push([id, group_name, group_display_name, group_description, id]);
    }

    // Setup - add a text input to each header cell
    $('#table thead tr').clone(true).addClass('filters').appendTo('#table thead');
    let searchColumns = [1, 2, 3, 4];

    $('#table').DataTable({
        dom: 'Brtip', buttons: {
            buttons: [{text: 'Export', extend: 'csv', filename: 'Groups Report', className: 'btn-export'}], dom: {
                button: {
                    className: 'btn'
                }
            }
        }, paginate: false,
        "language": {"emptyTable": "No data available in table"},
        "order": [[1, "asc"]],
        data: dataset,
        initComplete: function () {
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
        }, "autoWidth": false, "columnDefs": [{
            "width": "5%", orderable: false, className: "center", "targets": 0, "render": function (data, type, row) {
                return "<input type='checkbox' id='" + data + "' value='" + data + "'>";
            },
        }, {
            "width": "20%", "targets": 1, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 2, "render": function (data, type, row) {
                let colorClass = "";
                if (data === "yes") {
                    colorClass = " class='dataRed'"
                } else if (data === "no") {
                    colorClass = " class='dataGreen'"
                }
                return "<span" + colorClass + ">" + data + "</span>";
            },
        }, {
            "width": "50%", "targets": 3, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "15%", "targets": 4, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }]
    });
    $("#table_wrapper > .dt-buttons").prependTo("div.header-btns");
});
