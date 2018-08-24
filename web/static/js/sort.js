$(document).ready(function() {
  // call the tablesorter plugin
  $("table").tablesorter({
    // sort on the first column (hours) order asc
    sortList: [[0,0]]
  });
});
