let draw = false;

init();

/**
 * FUNCTIONS
 */

function init() {
  // initialize DataTables
  const table = $("#dt-table").DataTable( {
            "language": {
                //"url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
                "url": "//cdn.datatables.net/plug-ins/1.12.1/i18n/ru.json"
            },
            responsive: true,
        });
  // get table data
  const tableData = getTableData(table);
  // create Highcharts
  //createHighcharts(tableData);
  // table events
  setTableEvents(table);
}

function getTableData(table) {
  const dataArray = [],
    countryArray = [],
    populationArray = [],
    densityArray = [];

  // loop table rows
  table.rows({ search: "applied" }).every(function() {
    const data = this.data();
    countryArray.push(data[0]);
    populationArray.push(parseInt(data[1].replace(/\,/g, "")));
    densityArray.push(parseInt(data[2].replace(/\,/g, "")));
  });

  // store all data in dataArray
  dataArray.push(countryArray, populationArray, densityArray);

  return dataArray;
}
