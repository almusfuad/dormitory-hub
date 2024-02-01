const getParams = () => {
      const param = new URLSearchParams(window.location.search).get("slug");

      fetch
}


const details = (slug) => {

      console.log(slug);
      
      fetch(`/dormitory/list/?slug=${slug}`)
            .then((res) => res.json())
            .then((data) => {
                  console.log(data);
                  const queryParams = new URLSearchParams(data.slug).toString();
                  window.location.href =  `dormitory/dormitory_details.html?${queryParams}`;
            })
            .catch((err) => {
                  console.error(err);
            })
};