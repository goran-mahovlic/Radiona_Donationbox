<?php
$con=mysqli_connect("localhost",username,password,"donationbox");
// Check connection
if (mysqli_connect_errno()) {
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM moneyToProject");

echo "<table border='1'>
<tr>
<th>ID</th>
<th>Box Name</th>
<th>Project</th>
<th>Money</th>
<th>Last update</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
echo "<tr>";
echo "<td>" . $row['IDmoneyToProject'] . "</td>";
echo "<td>" . $row['BoxName'] . "</td>";
echo "<td>" . $row['project'] . "</td>";
echo "<td>" . $row['money'] . "</td>";
echo "<td>" . $row['UpdateDateTime'] . "</td>";
echo "</tr>";
}

echo "</table>";

mysqli_close($con);
?>