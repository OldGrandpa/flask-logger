<!DOCTYPE html>
<html>
<head>
    <title>Daily WhatsApp Logs</title>
</head>
<body>
    <h1>📋 Today's Logs</h1>

    <table border="1">
        <tr>
            <th>Device ID</th>
            <th>Phone Number</th>
            <th>Message Type</th>
            <th>Timestamp</th>
        </tr>
        {% for row in logs %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
        </tr>
        {% endfor %}
    </table>

    <br>
    <form action="/upload">
        <button type="submit">Upload Today's Log to Google Drive</button>
    </form>
</body>
</html>
