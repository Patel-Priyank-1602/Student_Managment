// Function to toggle between forms based on the selected action
function toggleForm() {
    const action = document.getElementById('actionSelect').value;
    const formContainers = document.querySelectorAll('.form-container');
    formContainers.forEach(form => form.style.display = 'none');

    if (action === 'insert') {
        document.getElementById('insertForm').style.display = 'block';
    } else if (action === 'search') {
        document.getElementById('searchForm').style.display = 'block';
    } else if (action === 'update') {
        document.getElementById('updateForm').style.display = 'block';
    } else if (action === 'delete') {
        document.getElementById('deleteForm').style.display = 'block';
    }
}

// Add student
document.getElementById('studentForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const data = {
        Roll_no: document.getElementById('roll_no').value,
        Name: document.getElementById('name').value,
        Branch: document.getElementById('branch').value,
        Sem: document.getElementById('sem').value,
        CGPA: document.getElementById('cgpa').value,
        Hobby: document.getElementById('hobby').value
    };

    fetch('http://localhost:5000/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => alert('Error: ' + error));
});

// Get student details
function getStudent() {
    const roll_no = document.getElementById('search_roll_no').value;

    fetch(`http://localhost:5000/get_student?Roll_no=${roll_no}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.Roll_no) {
            const detailsDiv = document.getElementById('studentDetails');
            detailsDiv.style.display = 'block';
            detailsDiv.innerHTML = `
                <p><strong>Roll No:</strong> ${data.Roll_no}</p>
                <p><strong>Name:</strong> ${data.Name}</p>
                <p><strong>Branch:</strong> ${data.Branch}</p>
                <p><strong>Semester:</strong> ${data.Sem}</p>
                <p><strong>CGPA:</strong> ${data.CGPA}</p>
                <p><strong>Hobby:</strong> ${data.Hobby}</p>
            `;
        } else {
            alert('Student not found!');
        }
    })
    .catch(error => alert('Error: ' + error));
}

// Update student
document.getElementById('updateForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const data = {
        Name: document.getElementById('update_name').value,
        Branch: document.getElementById('update_branch').value,
        Sem: document.getElementById('update_sem').value,
        CGPA: document.getElementById('update_cgpa').value,
        Hobby: document.getElementById('update_hobby').value
    };

    const roll_no = document.getElementById('update_roll_no').value;

    fetch(`http://localhost:5000/update_student?Roll_no=${roll_no}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => alert('Error: ' + error));
});

// Delete student
function deleteStudent() {
    const roll_no = document.getElementById('delete_roll_no').value;

    fetch(`http://localhost:5000/delete_student?Roll_no=${roll_no}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => alert('Error: ' + error));
}
