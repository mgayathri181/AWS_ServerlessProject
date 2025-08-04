const API_ENDPOINT = "https://46h95zvk83.execute-api.ca-central-1.amazonaws.com/prod";

// Function to fetch and display all orders
function fetchOrders() {
    $.ajax({
        url: API_ENDPOINT + "/orders",
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            let orders = [];

            try {
                if (response && typeof response.body === "string") {
                    orders = JSON.parse(response.body);
                } else if (Array.isArray(response)) {
                    orders = response;
                } else if (response && typeof response === "object" && response.body) {
                    orders = JSON.parse(response.body);
                } else {
                    alert("❌ Unexpected response format");
                    return;
                }
            } catch (e) {
                alert("❌ Failed to parse response body: " + e);
                return;
            }

            $("#ordersTable tbody").empty();

            if (orders.length > 0) {
                $("#ordersTable").show();
            } else {
                $("#ordersTable").hide();
            }

            orders.forEach(function (data) {
                $("#ordersTable tbody").append(
                    `<tr>
                        <td>${data.orderId || '-'}</td>
                        <td>${data.customerName || '-'}</td>
                        <td>${data.product_name || '-'}</td>
                        <td>${data.quantity || '-'}</td>
                        <td>${data.price || '-'}</td>
                    </tr>`
                );
            });
        },
        error: function () {
            alert("❌ Error fetching orders.");
        }
    });
}

// POST: Submit new order
document.getElementById("submitOrder").onclick = function () {
    const orderData = {
        orderId: document.getElementById("orderId").value,
        customerName: document.getElementById("customerName").value || "Unknown Customer",
        product_name: document.getElementById("product").value,
        quantity: parseInt(document.getElementById("quantity").value),
        price: parseFloat(document.getElementById("price").value)
    };

    $.ajax({
        url: API_ENDPOINT,
        type: "POST",
        data: JSON.stringify(orderData),
        contentType: "application/json; charset=utf-8",
        success: function () {
            alert("✅ Order submitted successfully!");
            fetchOrders();  // 🔁 Immediately refresh the list
        },
        error: function (error) {
            console.error("❌ Error submitting order:", error);
            alert("❌ Failed to submit order.");
        }
    });
};

// GET: When "View Orders" button clicked
document.getElementById("fetchOrders").onclick = fetchOrders;
