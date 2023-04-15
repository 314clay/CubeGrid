$(document).ready(function() {
    // Function to update the grid layout based on the search term
    function updateGrid(searchTerm) {
        $.ajax({
            url: "/update_grid",
            type: "POST",
            data: {search_term: searchTerm},
            success: function(data) {
                // Clear the grid container
                $("#grid-container").empty();
                // Add the filtered grid items to the container
                $.each(data, function(index, item) {
                    var gridItem = '<div class="col-md-3"><img src="' + item.image + '" alt="' + item.text + '"><h3>' + item.text + '</h3></div>';
                    $("#grid-container").append(gridItem);
                });
            }
        });
    }

    // Handle form submission
    $("#search-form").submit(function(event) {
        event.preventDefault();
        var searchTerm = $("#search").val();
        updateGrid(searchTerm);
    });

    // Initialize the grid with all items
    updateGrid("");
});
