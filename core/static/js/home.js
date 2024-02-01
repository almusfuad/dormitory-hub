// Fetch data from the API endpoint
const allDormitories = () => {
  fetch('/dormitories/list/')
.then((res) => res.json())
.then((data) => {
  console.log(data);
  const dormitoryContainer = document.getElementById('dormitory-container');
  
  // Loop through the data to create card elements
  data.forEach(dorm => {
    // Create card element
    const card = document.createElement('div');
    card.classList.add('col-md-4');

    // Create card content
    card.innerHTML = `
      <div class="card">
        <img src="${dorm.image}" class="card-img-top" alt="Dormitory Image">
        <div class="card-body">
          <h5 class="card-title">${dorm.name}</h5>
          <p class="card-text">Location: ${dorm.location.location}</p>
          <p class="card-text">Address: ${dorm.address}</p>
          <a class="btn btn-primary btn-lg" role="button" href="dormitory_details.html?${dorm.slug}">Details</a>
        </div>
      </div>
    `;

    console.log(dorm.slug);

    // Append card to dormitory container
    dormitoryContainer.appendChild(card);
  });

      
    })
    .catch( (err) => {
      console.error('Error fetching dormitory data:', err);
    });
};


allDormitories();