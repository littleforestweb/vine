/*
    Created on : 02 Mar 2022, 09:59:17
    Author     : xhico
*/

async function populateEditSiteDialog() {
    console.log("populateEditSiteDialog() START");

    let checked_items = $("input:checked");
    let n_checked_items = checked_items.length;
    let row = checked_items.parent().parent();

    console.log("n checked_items = " + checked_items.length);
    console.log("row html = " + row.html());
    console.log("row text = " + row.text());

    let spans = row.find("span");
    console.log("spans = " + spans.length);
    console.log(spans.text());

    let site_id = spans[0].textContent;
    let site_url = spans[1].textContent;
    let site_folder = spans[2].textContent;

    console.log("site_id : " + site_id);
    console.log("site_url : " + site_url);
    console.log("site_folder : " + site_folder);

    // Populate edit fields
    $('#e-site-id').val(site_id);
    $('#e-site-url').val(site_url);
    $('#e-site-folder').val(site_folder);

    // Populate hidden fields (for reference)
    $('#h-e-site-id').val(site_id);
    $('#h-e-site-url').val(site_url);
    $('#h-e-site-folder').val(site_folder);

    console.log("populateEditSiteDialog() END");
}

async function updateSite() {
    console.log("updateSite() START");

    let e_site_id = document.getElementById("e-site-id").value;
    let e_site_url = document.getElementById("e-site-url").value;
    let e_site_folder = document.getElementById("e-site-folder").value;

    let h_e_site_id = document.getElementById("h-e-site-id").value;
    let h_e_site_url = document.getElementById("h-e-site-url").value;
    let h_e_site_folder = document.getElementById("h-e-site-folder").value;

    console.log("Updating site from :");

    console.log("h_e_site_id : " + h_e_site_id);
    console.log("h_e_site_url : " + h_e_site_url);
    console.log("h_e_site_folder : " + h_e_site_folder);

    console.log("");

    console.log("Updating site to :");

    console.log("e_site_id : " + e_site_id);
    console.log("e_site_url : " + e_site_url);
    console.log("e_site_folder : " + e_site_folder);

    console.log("");

    // Post
    $.ajax({
        type: "POST", url: "/update/site", data: {
            "original_site_id": h_e_site_id, "original_site_url": h_e_site_url, "original_site_folder": h_e_site_folder,
            "new_site_id": e_site_id, "new_site_url": e_site_url, "new_site_folder": e_site_folder
        }, success: function (entry) {

            $('#editSiteModal').modal('hide');

            // Show success notification
            $('#editSiteSuccessNotification').toast('show');

            // Refresh page
            //setTimeout(function () {
            //    location.reload(true);
            //}, 2000);
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            $('#editSiteModal').modal('hide');

            // Show Error Modal
            $('#errorModal').modal('show');
        }
    });


    console.log("updateSite() END");
}

async function deleteSites() {
    console.log("deleteSites() START");

    let checked_sites = [];
    let checked_sites_str = "";

    $.each($("input:checked"), function (K, V) {
        checked_sites.push(V.value);
        checked_sites_str += V.value + ",";
        console.log("deleteSites() : END");
    });
    checked_sites_str = checked_sites_str.slice(0, -1);

    console.log("checked_sites_str : " + checked_sites_str);

    // Post
    $.ajax({
        type: "POST", url: "/delete/sites", data: {
            "sites_to_delete": checked_sites_str
        }, success: function (entry) {

            // Show success notification
            $('#deleteSitesSuccessNotification').toast('show');
            // Refresh page
            setTimeout(function () {
                location.reload(true);
            }, 2000);
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            // Hide Create Modal
            $('#deleteSitesModal').modal('hide');

            // Show Error Modal
            $('#errorDeleteModal').modal('show');

        }
    });

    console.log("deleteSite() END");
}

async function addSite() {
    $.ajax({
        type: "POST",
        url: "/add/site",
        data: {"base_url": document.getElementById("site-url").value},
        success: function (entry) {

            // Check for failed entry
            if (entry["message"] === "success") {
                // Add row to Table
                let id = entry["id"];
                let base_url = entry["base_url"];
                let base_folder = entry["base_folder"];
                let submitted_datetime = entry["submitted_datetime"].replace("GMT", "").trim();
                let status = entry["status"];
                $('#table').DataTable().row.add(["", id, base_url, base_folder, submitted_datetime, status, id]).order([1, 'desc']).draw();

                // Hide Create Modal
                $('#addSiteModal').modal('hide');

                // Show success notification
                $('#addSiteSuccessNotification').toast('show');
            } else {
                // Hide Create Modal
                $('#addSiteModal').modal('hide');

                // Show Error Modal
                $('#errorModal').modal('show');
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            // Hide Create Modal
            $('#addSiteModal').modal('hide');

            // Show Error Modal
            $('#errorModal').modal('show');
        }
    });
}

window.addEventListener('DOMContentLoaded', async function main() {
    console.log("Starting");
    console.log("Get All Sites");

    // Reset pagesTable
    $('#table').DataTable().clear().draw();
    $('#table').DataTable().destroy();

    // Get sitesJSON
    let json = await $.get("/api/get_sites", function (result) {
        return result;
    });

    // Set dataset
    let dataset = [];
    json = json["sites"];
    for (let i = 0; i < json.length; i++) {
        let entry = json[i];
        let id = entry["id"];
        let base_url = entry["base_url"];
        let base_folder = entry["base_folder"];
        let submitted_datetime = entry["submitted_datetime"].replace("GMT", "").trim();
        let status = entry["status"];
        dataset.push([id, id, base_url, base_folder, submitted_datetime, status, [id, status]]);
    }

    // Setup - add a text input to each header cell
    $('#table thead tr').clone(true).addClass('filters').appendTo('#table thead');
    let searchColumns = [1, 2, 3, 4, 5];

    // Initialize Errors Table
    $('#table').DataTable({
        dom: 'Brtip', buttons: {
            buttons: [{text: 'Export', extend: 'csv', filename: 'Sites Report', className: 'btn-export'}], dom: {
                button: {
                    className: 'btn'
                }
            }
        }, paginate: false,
        "language": {"emptyTable": "No data available in table"},
        "order": [[1, "desc"]],
        data: dataset,
        "autoWidth": false,
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
        },
        "columnDefs": [{
            "width": "5%", orderable: false, className: "center", "targets": 0, "render": function (data, type, row) {
                return "<input type='checkbox' id='" + data + "' value='" + data + "'>";
            },
        }, {
            "width": "5%", "targets": 1, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "40%", "targets": 2, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "10%", "targets": 3, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "20%", "targets": 4, "render": function (data, type, row) {
                return "<span>" + data + "</span>";
            },
        }, {
            "width": "15%", "targets": 5, "render": function (data, type, row) {
                let colorClass = "";
                data = data.toString();
                if (data.includes("complete")) {
                    colorClass = " class='dataGreen'"
                } else if (data.includes("running")) {
                    colorClass = " class='dataBlue'"
                } else if (data.includes("failed")) {
                    colorClass = " class='dataRed'"
                }
                return "<span" + colorClass + ">" + data + "</span>";
            },
        }, {
            "width": "5%", orderable: false, "targets": 6, "render": function (data, type, row) {
                if (data[1] === "complete") {
                    return "<a class='green-link' href='/get_site?id=" + data[0] + "'>View</a>";
                } else {
                    return "";
                }
            },
        }]
    });
    $("#table_wrapper > .dt-buttons").prependTo("div.header-btns");
});
