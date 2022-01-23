// as the search and pagination is not working properly in the url
//   when we reload the next or any page the search term from query / url gets disappear

// Get search form and page link
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// if search form exist
if (searchForm) {
  // adding event handler to every page-link
  for (let i = 0; pageLinks.length > i; i++) {
    pageLinks[i].addEventListener('click', function (e) {
      e.preventDefault()

      // Get the data attribute
      let page = this.dataset.page
      // console.log(page);

      // add hiddent search input to form
      searchForm.innerHTML += `<input value=${page} name="page" hidden />`
      // submit form
      searchForm.submit()
    })
  }
}
