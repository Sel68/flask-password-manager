function deletePassword(id) {
    fetch('/delete-password', {
        method: 'POST',
        body: JSON.stringify({ passwordId: id }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to delete password');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the password.');
    });
}